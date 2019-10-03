# -*- coding: utf-8 -*-
# Copyright: (c) 2019, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, response, utils,
)


class TestSync:
    def test_absent_no_current_object(self, mocker):
        client = mocker.Mock()
        client.get.return_value = response.Response(404, "")

        changed, object = utils.sync("absent", client, "/path", {}, False)

        assert changed is False
        assert object is None

    def test_absent_no_current_object_check(self, mocker):
        client = mocker.Mock()
        client.get.return_value = response.Response(404, "")

        changed, object = utils.sync("absent", client, "/path", {}, True)

        assert changed is False
        assert object is None

    def test_absent_current_object_present(self, mocker):
        client = mocker.Mock()
        client.get.return_value = response.Response(200, '{}')
        client.delete.return_value = response.Response(204, "")

        changed, object = utils.sync("absent", client, "/path", {}, False)

        assert changed is True
        assert object is None
        client.delete.assert_called_with("/path")

    def test_absent_current_object_present_check(self, mocker):
        client = mocker.Mock()
        client.get.return_value = response.Response(200, '{}')
        client.delete.return_value = response.Response(204, "")

        changed, object = utils.sync("absent", client, "/path", {}, True)

        assert changed is True
        assert object is None
        client.delete.assert_not_called()

    def test_present_no_current_object(self, mocker):
        client = mocker.Mock()
        client.get.side_effect = (
            response.Response(404, ""),
            response.Response(200, '{"new": "data"}'),
        )
        client.put.return_value = response.Response(201, "")

        changed, object = utils.sync(
            "present", client, "/path", {"my": "data"}, False,
        )

        assert changed is True
        assert {"new": "data"} == object
        client.put.assert_called_once_with("/path", {"my": "data"})

    def test_present_no_current_object_check(self, mocker):
        client = mocker.Mock()
        client.get.return_value = response.Response(404, "")

        changed, object = utils.sync(
            "present", client, "/path", {"my": "data"}, True,
        )

        assert changed is True
        assert {"my": "data"} == object
        client.put.assert_not_called()

    def test_present_current_object_differ(self, mocker):
        client = mocker.Mock()
        client.get.side_effect = (
            response.Response(200, '{"current": "data"}'),
            response.Response(200, '{"new": "data"}'),
        )
        client.put.return_value = response.Response(201, "")

        changed, object = utils.sync(
            "present", client, "/path", {"my": "data"}, False,
        )

        assert changed is True
        assert {"new": "data"} == object
        client.put.assert_called_once_with("/path", {"my": "data"})

    def test_present_current_object_differ_check(self, mocker):
        client = mocker.Mock()
        client.get.return_value = response.Response(200, '{"current": "data"}')

        changed, object = utils.sync(
            "present", client, "/path", {"my": "data"}, True,
        )

        assert changed is True
        assert {"my": "data"} == object
        client.put.assert_not_called()

    def test_present_current_object_does_not_differ(self, mocker):
        client = mocker.Mock()
        client.get.return_value = response.Response(200, '{"my": "data"}')

        changed, object = utils.sync(
            "present", client, "/path", {"my": "data"}, False,
        )

        assert changed is False
        assert {"my": "data"} == object
        client.put.assert_not_called()

    def test_present_current_object_does_not_differ_check(self, mocker):
        client = mocker.Mock()
        client.get.return_value = response.Response(200, '{"my": "data"}')

        changed, object = utils.sync(
            "present", client, "/path", {"my": "data"}, True,
        )

        assert changed is False
        assert {"my": "data"} == object
        client.put.assert_not_called()


class TestIsDifferentType:
    def test_different_types(self):
        assert not utils._is_same_type([1], 1)

    def test_different_string_types(self):
        assert utils._is_same_type(u'a', 'a')

    def test_special_chars_same_types(self):
        assert utils._is_same_type(u'£', '£')


class TestDoDiffer:
    @pytest.mark.parametrize("desired", [None, {"a": "b"}, 1, False, 2.3])
    def test_current_none_always_differ(self, desired):
        assert utils.do_differ(None, desired) is True

    def test_extra_keys_in_current_do_not_matter(self):
        assert utils.do_differ({"a": "b", "c": 3}, {"a": "b"}) is False

    def test_special_characters(self):
        assert utils.do_differ({"a": "£", "c": 3}, {"a": "£"}) is False

    def test_detect_different_values(self):
        assert utils.do_differ({"a": "b"}, {"a": "c"}) is True

    def test_detect_different_value_structure(self, mocker):
        debug_log = mocker.patch(
            "ansible_collections.sensu.sensu_go.plugins.module_utils.debug.log")
        assert utils.do_differ({"a": "b", "c": {"d": ["e"]}}, {"a": "b", "c": {"d": 1}}) is True
        debug_log.assert_called_once_with(
            "Remote and local value on key '{0}' structurally mismatch", "d")

    def test_detect_missing_keys_in_current(self, mocker):
        debug_log = mocker.patch(
            "ansible_collections.sensu.sensu_go.plugins.module_utils.debug.log")
        assert utils.do_differ({"a": "b"}, {"c": "d"}) is True
        debug_log.assert_not_called()

    def test_desired_none_values_are_ignored(self):
        assert utils.do_differ({"a": "b"}, {"c": None}) is False


class TestGet:
    @pytest.mark.parametrize(
        "status", [100, 201, 202, 203, 204, 400, 401, 403, 500, 501],
    )
    def test_abort_on_invalid_status(self, mocker, status):
        client = mocker.Mock()
        client.get.return_value = response.Response(status, "")

        with pytest.raises(errors.SyncError, match=str(status)):
            utils.get(client, "/get")
        client.get.assert_called_once_with("/get")

    def test_abort_on_invalid_json(self, mocker):
        client = mocker.Mock()
        client.get.return_value = response.Response(200, "")

        with pytest.raises(errors.SyncError, match="JSON"):
            utils.get(client, "/get")
        client.get.assert_called_once_with("/get")

    def test_ignore_invalid_json_on_404(self, mocker):
        client = mocker.Mock()
        client.get.return_value = response.Response(404, "")

        object = utils.get(client, "/get")

        assert object is None
        client.get.assert_called_once_with("/get")

    def test_valid_json(self, mocker):
        client = mocker.Mock()
        client.get.return_value = response.Response(200, '{"get": "data"}')

        object = utils.get(client, "/get")

        assert {"get": "data"} == object
        client.get.assert_called_once_with("/get")


class TestDelete:
    @pytest.mark.parametrize(
        "status", [100, 200, 201, 202, 203, 400, 401, 403, 500, 501],
    )
    def test_abort_on_invalid_status(self, mocker, status):
        client = mocker.Mock()
        client.delete.return_value = response.Response(status, "")

        with pytest.raises(errors.SyncError, match=str(status)):
            utils.delete(client, "/delete")
        client.delete.assert_called_once_with("/delete")

    def test_valid_delete(self, mocker):
        client = mocker.Mock()
        client.delete.return_value = response.Response(204, "{}")

        object = utils.delete(client, "/delete")

        assert object is None
        client.delete.assert_called_once_with("/delete")


class TestPut:
    @pytest.mark.parametrize(
        "status", [100, 200, 202, 203, 204, 400, 401, 403, 500, 501],
    )
    def test_abort_on_invalid_status(self, mocker, status):
        client = mocker.Mock()
        client.put.return_value = response.Response(status, "")

        with pytest.raises(errors.SyncError, match=str(status)):
            utils.put(client, "/put", {"payload": "data"})
        client.put.assert_called_once_with("/put", {"payload": "data"})

    def test_valid_put(self, mocker):
        client = mocker.Mock()
        client.put.return_value = response.Response(201, '{"put": "data"}')

        object = utils.put(client, "/put", {"payload": "data"})

        assert object is None
        client.put.assert_called_once_with("/put", {"payload": "data"})


class TestDictToSingleItemDicts:
    def test_conversion(self):
        result = utils.dict_to_single_item_dicts({"a": 0, 1: "b"})

        assert 2 == len(result)
        for item in ({"a": 0}, {1: "b"}):
            assert item in result


class TestDictToKeyValueString:
    def test_conversion(self):
        result = utils.dict_to_key_value_strings({"a": 0, 1: "b"})

        assert {"a=0", "1=b"} == set(result)
