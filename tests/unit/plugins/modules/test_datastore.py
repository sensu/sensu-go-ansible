from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, http,
)
from ansible_collections.sensu.sensu_go.plugins.modules import datastore

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
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
            spec=dict(dsn="my-dsn", pool_size=0, max_idle_conns=2, batch_buffer=0, batch_size=1, enable_round_robin=False, strict=False),
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
            spec=dict(dsn="my-dsn", pool_size=543, max_idle_conns=2, batch_buffer=0, batch_size=1, enable_round_robin=False, strict=False),
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


class TestDatastoreParams(ModuleTestCase):
    @pytest.mark.parametrize(
        # name                              ... Resource name
        # state                             ... Prefered resource state (Present/Absent)
        # dsn                               ... url or postgre connection string
        # pool_size                         ... max number of connections
        # max_conn_lifetime                 ... max time a connection can persist
        # max_idle_conns                    ... max number of idle connections
        # batch_workers                     ... number of GOroutines
        # batch_buffer                      ... max requests to buffer in memory
        # batch_size                        ... number of requests in each transaction
        # enable_round_robin                ... round robin (True/False)
        # strict                            ... strict (True/False)
        # expected_payload                  ... expected payload
        ("name", "state", "dsn", "pool_size", "max_conn_lifetime", "max_idle_conns", "batch_workers",
         "batch_buffer", "batch_size", "enable_round_robin", "strict", "expected_payload"),
        [
            # Present
            ("my_resource", "present", "postgresql://user:secret@host:port/dbname", 2, 1, 1, 1, 1, 1,
             False, True,
                {'type': 'PostgresConfig', 'api_version': 'store/v1', 'metadata': {'name': 'my_resource'},
                    'spec':
                        {
                            'dsn': 'postgresql://user:secret@host:port/dbname', 'pool_size': 2, 'max_conn_lifetime': '1',
                            'max_idle_conns': 1, 'batch_workers': 1, 'batch_buffer': 1, 'batch_size': 1,
                            'enable_round_robin': False, 'strict': True}}),

            ("another_resource", "present", "postgresql://user:secret@host:port/dbname", 0, 0, 0, 0, 0, 0,
             False, False,
                {'type': 'PostgresConfig', 'api_version': 'store/v1', 'metadata': {'name': 'another_resource'},
                    'spec':
                        {
                            'dsn': 'postgresql://user:secret@host:port/dbname', 'pool_size': 0, 'max_conn_lifetime': '0',
                            'max_idle_conns': 0, 'batch_workers': 0, 'batch_buffer': 0, 'batch_size': 0,
                            'enable_round_robin': False, 'strict': False}}),
            # Absent
            ("my_resource", "absent", "", None, None, None, None, None, None,
             False, True,
                {'type': 'PostgresConfig', 'api_version': 'store/v1', 'metadata': {'name': 'my_resource'},
                    'spec':
                        {
                            'dsn': '', 'enable_round_robin': False, 'strict': True}}),

            ("my_resource", "absent", "postgresql://user:secret@host:port/dbname", 2, 1, 1, 1, 2, 3,
             False, True,
                {'type': 'PostgresConfig', 'api_version': 'store/v1', 'metadata': {'name': 'my_resource'},
                    'spec':
                        {
                            'dsn': 'postgresql://user:secret@host:port/dbname', 'pool_size': 2, 'max_conn_lifetime': '1',
                            'max_idle_conns': 1, 'batch_workers': 1, 'batch_buffer': 2, 'batch_size': 3,
                            'enable_round_robin': False, 'strict': True}}),
        ],
    )
    def test_parameters_datastore(self, mocker, name, state, dsn, pool_size, max_conn_lifetime, max_idle_conns, batch_workers,
                                  batch_buffer, batch_size, enable_round_robin, strict, expected_payload):
        sync_mock = mocker.patch.object(datastore, "sync")
        sync_mock.return_value = True, {}
        set_module_args(
            name=name,
            dsn=dsn,
            state=state,
            pool_size=pool_size,
            max_conn_lifetime=max_conn_lifetime,
            max_idle_conns=max_idle_conns,
            batch_workers=batch_workers,
            batch_buffer=batch_buffer,
            batch_size=batch_size,
            enable_round_robin=enable_round_robin,
            strict=strict,
        )
        with pytest.raises(AnsibleExitJson):
            datastore.main()
        state_test, _client_test, list_path_test, resource_path_test, payload_test, check_mode_test = (
            sync_mock.call_args[0]
        )
        assert state_test == state
        assert payload_test == expected_payload
