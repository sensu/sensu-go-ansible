from __future__ import absolute_import, division, print_function
__metaclass__ = type

import sys

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, http,
)
from ansible_collections.sensu.sensu_go.plugins.modules import tessen

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestSync:
    def test_remote_and_desired_equal(self, mocker):
        client = mocker.Mock()
        client.get.return_value = http.Response(200, '{}')
        changed, object = tessen.sync(client, "/path", {}, False)

        assert changed is False
        assert object == {}

    def test_remote_and_desired_not_equal(self, mocker):
        client = mocker.Mock()
        client.get.side_effect = (
            http.Response(200, '{"opt_out": "false"}'),
            http.Response(200, '{"opt_out": "true"}'),
        )
        client.put.return_value = http.Response(200, "")
        changed, object = tessen.sync(client, "/path", {'opt_out': True}, False)

        assert changed is True
        assert object == {'opt_out': 'true'}
        client.put.assert_called_once_with("/path", {'opt_out': True})

    def test_remote_and_desired_equal_check(self, mocker):
        client = mocker.Mock()
        client.get.return_value = http.Response(200, '{}')
        changed, object = tessen.sync(client, "/path", {}, True)

        assert changed is False
        assert object == {}

    def test_remote_and_desired_not_equal_check(self, mocker):
        client = mocker.Mock()
        client.get.return_value = http.Response(200, '{"opt_out": "false"}')
        changed, object = tessen.sync(client, "/path", {'opt_out': True}, True)

        assert changed is True
        assert object == {'opt_out': True}
        client.put.assert_not_called()


class TestTessen(ModuleTestCase):
    def test_enabled(self, mocker):
        sync_mock = mocker.patch.object(tessen, 'sync')
        sync_mock.return_value = True, {}
        set_module_args(
            state='enabled'
        )

        with pytest.raises(AnsibleExitJson):
            tessen.main()

        _client, path, payload, check_mode = sync_mock.call_args[0]
        assert path == '/api/core/v2/tessen'
        assert payload == dict(
            opt_out=False
        )
        assert check_mode is False

    def test_disabled(self, mocker):
        sync_mock = mocker.patch.object(tessen, 'sync')
        sync_mock.return_value = True, {}
        set_module_args(
            state='disabled'
        )

        with pytest.raises(AnsibleExitJson):
            tessen.main()

        _client, path, payload, check_mode = sync_mock.call_args[0]
        assert path == '/api/core/v2/tessen'
        assert payload == dict(
            opt_out=True
        )
        assert check_mode is False

    def test_failure(self, mocker):
        sync_mock = mocker.patch.object(tessen, 'sync')
        sync_mock.side_effect = errors.Error('Bad error')
        set_module_args(
            state='enabled'
        )

        with pytest.raises(AnsibleFailJson):
            tessen.main()
