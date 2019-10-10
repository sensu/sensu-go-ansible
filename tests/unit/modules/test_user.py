from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, response, utils
)
from ansible_collections.sensu.sensu_go.plugins.modules import user

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)


class TestSync:
    def test_no_current_object(self, mocker):
        client = mocker.Mock()
        client.get.return_value = response.Response(200, '{"new": "data"}')
        client.put.return_value = response.Response(201, '')

        changed, object = user.sync(
            None, 'disabled', client, '/path', {'my': 'data'}, False
        )

        assert changed is True
        assert {'new': 'data'} == object
        client.put.assert_called_once_with('/path', {'my': 'data'})

    def test_no_current_object_check(self, mocker):
        client = mocker.Mock()
        client.get.return_value = response.Response(200, '{"new": "data"}')

        changed, object = user.sync(
            None, 'disabled', client, '/path', {'my': 'data'}, True
        )

        assert changed is True
        assert {'my': 'data'} == object
        client.put.assert_not_called()

    def test_disabled_current_object_present(self, mocker):
        client = mocker.Mock()
        client.get.return_value = response.Response(200, '{"current": "data"}')
        client.delete.return_value = response.Response(204, '')

        changed, object = user.sync(
            {}, 'disabled', client, '/path', {}, False
        )
        assert changed is True
        assert object is not None
        client.delete.assert_called_with('/path')

    def test_disabled_current_object_present_check(self, mocker):
        client = mocker.Mock()
        client.get.return_value = response.Response(200, '{"current": "data"}')
        client.delete.return_value = response.Response(204, '')

        changed, object = user.sync(
            {}, 'disabled', client, '/path', {}, True
        )
        assert changed is True
        assert object is not None
        client.delete.assert_not_called()

    def test_current_object_does_not_differ(self, mocker):
        client = mocker.Mock()

        changed, object = user.sync(
            {'my': 'data'}, 'present', client, '/path', {'my': 'data'}, False,
        )

        assert changed is False
        assert {'my': 'data'} == object
        client.put.assert_not_called()

    def test_current_object_does_not_differ_check(self, mocker):
        client = mocker.Mock()

        changed, object = user.sync(
            {'my': 'data'}, 'present', client, '/path', {'my': 'data'}, True,
        )

        assert changed is False
        assert {'my': 'data'} == object
        client.put.assert_not_called()


class TestUser(ModuleTestCase):
    def test_minimal_user_parameters(self, mocker):
        get_mock = mocker.patch.object(utils, 'get')
        get_mock.return_value = None
        sync_mock = mocker.patch.object(user, 'sync')
        sync_mock.return_value = True, {}
        set_module_args(
            name='alice',
            password='alice!?pass',
        )

        with pytest.raises(AnsibleExitJson):
            user.main()

        object, state, _client, path, payload, check_mode = sync_mock.call_args[0]
        assert state == 'enabled'
        assert path == '/users/alice'
        assert payload == dict(
            username='alice',
            password='alice!?pass',
            disabled=False
        )
        assert check_mode is False

    def test_all_user_parameters(self, mocker):
        get_mock = mocker.patch.object(utils, 'get')
        get_mock.return_value = None
        sync_mock = mocker.patch.object(user, 'sync')
        sync_mock.return_value = True, {}
        set_module_args(
            name='test_user',
            state='disabled',
            password='password',
            groups=['dev', 'ops'],
        )

        with pytest.raises(AnsibleExitJson):
            user.main()

        object, state, _client, path, payload, check_mode = sync_mock.call_args[0]
        assert state == 'disabled'
        assert path == '/users/test_user'
        assert payload == dict(
            username='test_user',
            password='password',
            groups=['dev', 'ops'],
            disabled=True
        )
        assert check_mode is False

    def test_disable_non_existent_user(self, mocker):
        get_mock = mocker.patch.object(utils, 'get')
        get_mock.return_value = None
        set_module_args(
            name='test_user',
            state='disabled',
            groups=['dev', 'ops'],
        )

        with pytest.raises(AnsibleFailJson, match='Cannot disable a non existent user'):
            user.main()

    def test_failure(self, mocker):
        get_mock = mocker.patch.object(utils, 'get')
        get_mock.return_value = None
        sync_mock = mocker.patch.object(user, 'sync')
        sync_mock.side_effect = errors.Error('Bad error')
        set_module_args(
            name='test_user',
            password='password'
        )

        with pytest.raises(AnsibleFailJson):
            user.main()
