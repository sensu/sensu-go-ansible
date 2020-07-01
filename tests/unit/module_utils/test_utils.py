# -*- coding: utf-8 -*-
# Copyright: (c) 2019, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, http, utils,
)


class TestSync:
    def test_absent_no_current_object(self, mocker):
        client = mocker.Mock()
        client.get.return_value = http.Response(404, "")

        changed, object = utils.sync("absent", client, "/path", {}, False)

        assert changed is False
        assert object is None

    def test_absent_no_current_object_check(self, mocker):
        client = mocker.Mock()
        client.get.return_value = http.Response(404, "")

        changed, object = utils.sync("absent", client, "/path", {}, True)

        assert changed is False
        assert object is None

    def test_absent_current_object_present(self, mocker):
        client = mocker.Mock()
        client.get.return_value = http.Response(200, '{}')
        client.delete.return_value = http.Response(204, "")

        changed, object = utils.sync("absent", client, "/path", {}, False)

        assert changed is True
        assert object is None
        client.delete.assert_called_with("/path")

    def test_absent_current_object_present_check(self, mocker):
        client = mocker.Mock()
        client.get.return_value = http.Response(200, '{}')
        client.delete.return_value = http.Response(204, "")

        changed, object = utils.sync("absent", client, "/path", {}, True)

        assert changed is True
        assert object is None
        client.delete.assert_not_called()

    def test_present_no_current_object(self, mocker):
        client = mocker.Mock()
        client.get.side_effect = (
            http.Response(404, ""),
            http.Response(200, '{"new": "data"}'),
        )
        client.put.return_value = http.Response(201, "")

        changed, object = utils.sync(
            "present", client, "/path", {"my": "data"}, False,
        )

        assert changed is True
        assert {"new": "data"} == object
        client.put.assert_called_once_with("/path", {"my": "data"})

    def test_present_no_current_object_check(self, mocker):
        client = mocker.Mock()
        client.get.return_value = http.Response(404, "")

        changed, object = utils.sync(
            "present", client, "/path", {"my": "data"}, True,
        )

        assert changed is True
        assert {"my": "data"} == object
        client.put.assert_not_called()

    def test_present_current_object_differ(self, mocker):
        client = mocker.Mock()
        client.get.side_effect = (
            http.Response(200, '{"current": "data"}'),
            http.Response(200, '{"new": "data"}'),
        )
        client.put.return_value = http.Response(201, "")

        changed, object = utils.sync(
            "present", client, "/path", {"my": "data"}, False,
        )

        assert changed is True
        assert {"new": "data"} == object
        client.put.assert_called_once_with("/path", {"my": "data"})

    def test_present_current_object_differ_check(self, mocker):
        client = mocker.Mock()
        client.get.return_value = http.Response(200, '{"current": "data"}')

        changed, object = utils.sync(
            "present", client, "/path", {"my": "data"}, True,
        )

        assert changed is True
        assert {"my": "data"} == object
        client.put.assert_not_called()

    def test_present_current_object_does_not_differ(self, mocker):
        client = mocker.Mock()
        client.get.return_value = http.Response(200, '{"my": "data"}')

        changed, object = utils.sync(
            "present", client, "/path", {"my": "data"}, False,
        )

        assert changed is False
        assert {"my": "data"} == object
        client.put.assert_not_called()

    def test_present_current_object_does_not_differ_check(self, mocker):
        client = mocker.Mock()
        client.get.return_value = http.Response(200, '{"my": "data"}')

        changed, object = utils.sync(
            "present", client, "/path", {"my": "data"}, True,
        )

        assert changed is False
        assert {"my": "data"} == object
        client.put.assert_not_called()


class TestDoDiffer:
    def test_extra_keys_in_current_do_not_matter(self):
        assert utils.do_differ({"a": "b", "c": 3}, {"a": "b"}) is False

    def test_detect_different_values(self):
        assert utils.do_differ({"a": "b"}, {"a": "c"}) is True

    def test_detect_missing_keys_in_current(self):
        assert utils.do_differ({"a": "b"}, {"c": "d"}) is True

    def test_desired_none_values_are_ignored(self):
        assert utils.do_differ({"a": "b"}, {"c": None}) is False

    def test_metadata_ignores_created_by(self):
        assert utils.do_differ(
            dict(metadata=dict(a=1, created_by=2)),
            dict(metadata=dict(a=1)),
        ) is False

    def test_metadata_detects_change(self):
        assert utils.do_differ(
            dict(metadata=dict(a=1)), dict(metadata=dict(a=2)),
        ) is True

    def test_metadata_detects_change_in_presence_of_created_by(self):
        assert utils.do_differ(
            dict(metadata=dict(a=1, created_by=2)),
            dict(metadata=dict(a=2)),
        ) is True

    def test_ignore_keys_do_not_affect_the_outcome(self):
        assert utils.do_differ(dict(a=1), dict(a=2), "a") is False

    def test_ignore_keys_do_not_mask_other_differences(self):
        assert utils.do_differ(dict(a=1, b=1), dict(a=2, b=2), "a") is True


class TestGet:
    @pytest.mark.parametrize(
        "status", [100, 201, 202, 203, 204, 400, 401, 403, 500, 501],
    )
    def test_abort_on_invalid_status(self, mocker, status):
        client = mocker.Mock()
        client.get.return_value = http.Response(status, "")

        with pytest.raises(errors.SyncError, match=str(status)):
            utils.get(client, "/get")
        client.get.assert_called_once_with("/get")

    def test_abort_on_invalid_json(self, mocker):
        client = mocker.Mock()
        client.get.return_value = http.Response(200, "")

        with pytest.raises(errors.SyncError, match="JSON"):
            utils.get(client, "/get")
        client.get.assert_called_once_with("/get")

    def test_ignore_invalid_json_on_404(self, mocker):
        client = mocker.Mock()
        client.get.return_value = http.Response(404, "")

        object = utils.get(client, "/get")

        assert object is None
        client.get.assert_called_once_with("/get")

    def test_valid_json(self, mocker):
        client = mocker.Mock()
        client.get.return_value = http.Response(200, '{"get": "data"}')

        object = utils.get(client, "/get")

        assert {"get": "data"} == object
        client.get.assert_called_once_with("/get")


class TestDelete:
    @pytest.mark.parametrize(
        "status", [100, 200, 201, 202, 203, 400, 401, 403, 500, 501],
    )
    def test_abort_on_invalid_status(self, mocker, status):
        client = mocker.Mock()
        client.delete.return_value = http.Response(status, "")

        with pytest.raises(errors.SyncError, match=str(status)):
            utils.delete(client, "/delete")
        client.delete.assert_called_once_with("/delete")

    def test_valid_delete(self, mocker):
        client = mocker.Mock()
        client.delete.return_value = http.Response(204, "{}")

        object = utils.delete(client, "/delete")

        assert object is None
        client.delete.assert_called_once_with("/delete")


class TestPut:
    @pytest.mark.parametrize(
        "status", [100, 202, 203, 204, 400, 401, 403, 500, 501],
    )
    def test_abort_on_invalid_status(self, mocker, status):
        client = mocker.Mock()
        client.put.return_value = http.Response(status, "")

        with pytest.raises(errors.SyncError, match=str(status)):
            utils.put(client, "/put", {"payload": "data"})
        client.put.assert_called_once_with("/put", {"payload": "data"})

    @pytest.mark.parametrize("status", [200, 201])
    def test_valid_put(self, mocker, status):
        client = mocker.Mock()
        client.put.return_value = http.Response(status, '{"put": "data"}')

        object = utils.put(client, "/put", {"payload": "data"})

        assert object is None
        client.put.assert_called_once_with("/put", {"payload": "data"})


class TestDictToSingleItemDicts:
    def test_conversion(self):
        result = utils.dict_to_single_item_dicts({"a": 0, 1: "b"})

        assert 2 == len(result)
        for item in ({"a": 0}, {1: "b"}):
            assert item in result


class TestSingleItemDictsToDict:
    def test_conversion(self):
        assert dict(a=3, b=4, c=5) == utils.single_item_dicts_to_dict(
            [dict(a=3), dict(b=4), dict(c=5)]
        )


class TestDictToKeyValueString:
    def test_conversion(self):
        result = utils.dict_to_key_value_strings({"a": 0, 1: "b"})

        assert {"a=0", "1=b"} == set(result)


class TestBuildUrlPath:
    @pytest.mark.parametrize("parts,expectation", [
        ((), "/"),
        ((None, None), "/"),
        ((None, "a", "b", None, None, "c"), "/a/b/c"),
        (("get/rid of+stuff",), "/get%2Frid%20of%2Bstuff"),
        (("/", " ", "a"), "/%2F/%20/a"),
    ])
    def test_build_url_path_no_namespace(self, parts, expectation):
        path = "/api/enterprise/store/v1" + expectation
        assert path == utils.build_url_path(
            "enterprise/store", "v1", None, *parts
        )

    @pytest.mark.parametrize("parts,expectation", [
        ((), "/"),
        ((None, None), "/"),
        ((None, "a", "b", None, None, "c"), "/a/b/c"),
        (("get/rid of+stuff",), "/get%2Frid%20of%2Bstuff"),
        (("/", " ", "a"), "/%2F/%20/a"),
    ])
    def test_build_url_path_with_namespace(self, parts, expectation):
        path = "/api/core/v2/namespaces/default" + expectation
        assert path == utils.build_url_path(
            "core", "v2", "default", *parts
        )


class TestBuildCoreV2Path:
    def test_build_path_no_namespace(self):
        assert utils.build_core_v2_path(None, "a").startswith(
            "/api/core/v2/",
        )

    def test_build_url_with_namespace(self):
        assert utils.build_core_v2_path("default", "a").startswith(
            "/api/core/v2/namespaces/default/",
        )


class TestPrepareResultList:
    @pytest.mark.parametrize("input,output", [
        (None, []),  # this is mosti likely result of a 404 status
        ("a", ["a"]),
        ([], []),
        ([1, 2, 3], [1, 2, 3]),
        ([None], [None]),  # we leave lists intact, even if they contain None
    ])
    def test_list_construction(self, input, output):
        assert output == utils.prepare_result_list(input)


class TestConvertV1ToV2Response:
    def test_none_passes_through(self):
        assert utils.convert_v1_to_v2_response(None) is None

    def test_spec_only_if_metadata_is_missing(self):
        assert utils.convert_v1_to_v2_response(dict(
            spec=dict(a=1, b=2),
        )) == dict(a=1, b=2)

    def test_add_metadata_from_toplevel(self):
        assert utils.convert_v1_to_v2_response(dict(
            metadata=dict(name="sample"),
            spec=dict(a=1, b=2),
        )) == dict(metadata=dict(name="sample"), a=1, b=2)
