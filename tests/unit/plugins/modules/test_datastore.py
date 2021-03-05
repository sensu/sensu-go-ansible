from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, http,
)
from ansible_collections.sensu.sensu_go.plugins.modules import datastore

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)


class TestSync(ModuleTestCase):
    def test_absent_no_current_object(self, mocker):
        client = mocker.Mock()
        client.get.return_value = http.Response(404, "")

        changed, object = datastore.sync(
            "absent", client, "/list", "/resource", {}, False,
        )

        assert changed is False
        assert object is None

    def test_absent_no_current_object_check(self, mocker):
        client = mocker.Mock()
        client.get.return_value = http.Response(404, "")

        changed, object = datastore.sync(
            "absent", client, "/list", "/resource", {}, True,
        )

        assert changed is False
        assert object is None

    def test_absent_current_object_present(self, mocker):
        client = mocker.Mock()
        client.get.return_value = http.Response(200, '{}')
        client.delete.return_value = http.Response(204, "")

        changed, object = datastore.sync(
            "absent", client, "/list", "/resource", {}, False,
        )

        assert changed is True
        assert object is None
        client.delete.assert_called_with("/resource")

    def test_absent_current_object_present_check(self, mocker):
        client = mocker.Mock()
        client.get.return_value = http.Response(200, '{}')
        client.delete.return_value = http.Response(204, "")

        changed, object = datastore.sync(
            "absent", client, "/list", "/resource", {}, True,
        )

        assert changed is True
        assert object is None
        client.delete.assert_not_called()

    def test_present_current_object_differ(self, mocker):
        client = mocker.Mock()
        client.get.side_effect = (
            http.Response(200, '{"spec": {"current": "data"}}'),
            http.Response(200, '{"spec": {"new": "data"}}'),
        )
        client.put.return_value = http.Response(201, "")

        changed, object = datastore.sync(
            "present", client, "/list", "/resource", {"spec": {"my": "data"}},
            False,
        )

        assert changed is True
        assert {"new": "data"} == object
        client.put.assert_called_once_with(
            "/resource", {"spec": {"my": "data"}},
        )

    def test_present_current_object_differ_check(self, mocker):
        client = mocker.Mock()
        client.get.return_value = (
            http.Response(200, '{"spec": {"current": "data"}}')
        )

        changed, object = datastore.sync(
            "present", client, "/list", "/resource", {"spec": {"my": "data"}},
            True,
        )

        assert changed is True
        assert {"my": "data"} == object
        client.put.assert_not_called()

    def test_present_current_object_does_not_differ(self, mocker):
        client = mocker.Mock()
        client.get.return_value = (
            http.Response(200, '{"spec": {"my": "data"}}')
        )

        changed, object = datastore.sync(
            "present", client, "/list", "/resource", {"spec": {"my": "data"}},
            False,
        )

        assert changed is False
        assert {"my": "data"} == object
        client.put.assert_not_called()

    def test_present_current_object_does_not_differ_check(self, mocker):
        client = mocker.Mock()
        client.get.return_value = (
            http.Response(200, '{"spec": {"my": "data"}}')
        )

        changed, object = datastore.sync(
            "present", client, "/list", "/resource", {"spec": {"my": "data"}},
            True,
        )

        assert changed is False
        assert {"my": "data"} == object
        client.put.assert_not_called()

    def test_present_no_current_object_empty_backend(self, mocker):
        client = mocker.Mock()
        client.get.side_effect = (
            http.Response(404, ""),
            http.Response(200, "[]"),
            http.Response(200, '{"spec": {"new": "data"}}'),
        )
        client.put.return_value = http.Response(201, "")

        changed, object = datastore.sync(
            "present", client, "/list", "/resource", {"spec": {"my": "data"}},
            False,
        )

        assert changed is True
        assert {"new": "data"} == object
        client.put.assert_called_once_with(
            "/resource", {"spec": {"my": "data"}},
        )

    def test_present_no_current_object_empty_backend_check(self, mocker):
        client = mocker.Mock()
        client.get.side_effect = (
            http.Response(404, ""),
            http.Response(200, "[]"),
        )

        changed, object = datastore.sync(
            "present", client, "/list", "/resource", {"spec": {"my": "data"}},
            True,
        )

        assert changed is True
        assert {"my": "data"} == object
        client.put.assert_not_called()

    @pytest.mark.parametrize("check", [False, True])
    def test_present_no_current_object_non_empty_backend(self, mocker, check):
        client = mocker.Mock()
        client.get.side_effect = (
            http.Response(404, ""),
            http.Response(200, "[{}]"),
        )

        with pytest.raises(errors.Error, match="already active"):
            datastore.sync(
                "present", client, "/list", "/resource",
                {"spec": {"my": "data"}}, check,
            )

        client.put.assert_not_called()


class TestDatastore(ModuleTestCase):
    def test_minimal_datastore_parameters_present(self, mocker):
        sync_mock = mocker.patch.object(datastore, "sync")
        sync_mock.return_value = True, {}
        set_module_args(
            name="test_datastore",
            dsn="my-dsn",
        )

        with pytest.raises(AnsibleExitJson):
            datastore.main()

        state, _client, list_path, resource_path, payload, check_mode = (
            sync_mock.call_args[0]
        )
        assert state == "present"
        assert resource_path == "/api/enterprise/store/v1/provider/test_datastore"
        assert list_path == "/api/enterprise/store/v1/provider"
        assert payload == dict(
            type="PostgresConfig",
            api_version="store/v1",
            metadata=dict(name="test_datastore"),
            spec=dict(dsn="my-dsn"),
        )
        assert check_mode is False

    def test_minimal_datastore_parameters_absent(self, mocker):
        sync_mock = mocker.patch.object(datastore, "sync")
        sync_mock.return_value = True, {}
        set_module_args(
            name="test_datastore",
            state="absent",
        )

        with pytest.raises(AnsibleExitJson):
            datastore.main()

        state, _client, list_path, resource_path, _payload, check_mode = (
            sync_mock.call_args[0]
        )
        assert state == "absent"
        assert resource_path == "/api/enterprise/store/v1/provider/test_datastore"
        assert list_path == "/api/enterprise/store/v1/provider"
        assert check_mode is False

    def test_all_datastore_parameters(self, mocker):
        sync_mock = mocker.patch.object(datastore, "sync")
        sync_mock.return_value = True, {}
        set_module_args(
            name="test_datastore",
            dsn="my-dsn",
            pool_size=543,
        )

        with pytest.raises(AnsibleExitJson):
            datastore.main()

        state, _client, list_path, resource_path, payload, check_mode = (
            sync_mock.call_args[0]
        )
        assert state == "present"
        assert resource_path == "/api/enterprise/store/v1/provider/test_datastore"
        assert list_path == "/api/enterprise/store/v1/provider"
        assert payload == dict(
            type="PostgresConfig",
            api_version="store/v1",
            metadata=dict(name="test_datastore"),
            spec=dict(dsn="my-dsn", pool_size=543),
        )
        assert check_mode is False

    def test_failure(self, mocker):
        sync_mock = mocker.patch.object(datastore, "sync")
        sync_mock.side_effect = errors.Error("Bad error")
        set_module_args(
            name="test_datastore",
            dsn="my-dsn",
        )

        with pytest.raises(AnsibleFailJson):
            datastore.main()
