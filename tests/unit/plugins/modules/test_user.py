from __future__ import absolute_import, division, print_function
__metaclass__ = type

import sys

from distutils import version

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    arguments, errors, http, utils
)
from ansible_collections.sensu.sensu_go.plugins.modules import user

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestUpdatePassword:
    @pytest.mark.parametrize('check', [False, True])
    def test_password_is_valid(self, mocker, check):
        client = mocker.Mock()
        client.validate_auth_data.return_value = True

        changed = user.update_password(client, '/path', 'user', 'pass', check)

        assert changed is False
        client.validate_auth_data.assert_called_once_with('user', 'pass')
        client.put.assert_not_called()

    def test_password_is_invalid_older_than_5_21_0(self, mocker):
        client = mocker.Mock()
        client.validate_auth_data.return_value = False
        client.version = version.StrictVersion("5.20.2")
        client.put.return_value = http.Response(201, '')

        changed = user.update_password(client, '/path', 'user', 'pass', False)

        assert changed is True
        client.validate_auth_data.assert_called_once_with('user', 'pass')
        client.put.assert_called_once_with('/path/password', dict(
            username='user', password='pass',
        ))

    def test_password_is_invalid_5_21_0_or_newer(self, mocker):
        client = mocker.Mock()
        client.validate_auth_data.return_value = False
        client.version = version.StrictVersion("5.21.0")
        client.put.return_value = http.Response(201, '')

        changed = user.update_password(client, '/path', 'user', 'pass', False)

        assert changed is True
        client.validate_auth_data.assert_called_once_with('user', 'pass')
        client.put.assert_called_once()

        path, payload = client.put.call_args[0]
        assert path == '/path/reset_password'
        assert payload['username'] == 'user'

        # (tadeboro): We cannot validate the value without mocking the bcrypt.
        # And I would rather see that our code gets tested by actually using
        # the bcrypt rather than mocking it out. This way, the message
        # encode/decode stuff gets put through its paces.
        assert 'password_hash' in payload

    def test_password_is_invalid_check_mode(self, mocker):
        client = mocker.Mock()
        client.validate_auth_data.return_value = False

        changed = user.update_password(client, '/path', 'user', 'pass', True)

        assert changed is True
        client.validate_auth_data.assert_called_once_with('user', 'pass')
        client.put.assert_not_called()


class TestUpdatePasswordHash:
    @pytest.mark.parametrize('check', [False, True])
    def test_sensu_go_older_than_5_21_0(self, mocker, check):
        client = mocker.Mock()
        client.version = version.StrictVersion("5.20.0")

        with pytest.raises(errors.SensuError):
            user.update_password_hash(client, '/path', 'user', 'hash', check)

        client.put.assert_not_called()

    def test_sensu_go_newer_than_5_21_0(self, mocker):
        client = mocker.Mock()
        client.version = version.StrictVersion("5.21.0")
        client.put.return_value = http.Response(201, '')

        changed = user.update_password_hash(
            client, '/path', 'user', 'hash', False,
        )

        assert changed is True
        client.put.assert_called_once()

        path, payload = client.put.call_args[0]
        assert path == '/path/reset_password'
        assert payload['username'] == 'user'
        assert payload['password_hash'] == 'hash'

    def test_sensu_go_newer_than_5_21_0_check_mode(self, mocker):
        client = mocker.Mock()
        client.version = version.StrictVersion("5.21.0")

        changed = user.update_password_hash(
            client, '/path', 'user', 'pass', True,
        )

        assert changed is True
        client.put.assert_not_called()


class TestUpdateGroups:
    @pytest.mark.parametrize('check', [False, True])
    def test_update_groups_no_change(self, mocker, check):
        client = mocker.Mock()

        result = user.update_groups(
            client, '/path', ['a', 'b'], ['b', 'a'], check,
        )

        assert result is False
        client.put.assert_not_called()
        client.delete.assert_not_called()

    def test_update_groups(self, mocker):
        client = mocker.Mock()
        client.put.side_effect = [
            http.Response(201, ''), http.Response(201, ''),
        ]
        client.delete.side_effect = [
            http.Response(204, ''), http.Response(204, ''),
        ]

        result = user.update_groups(
            client, '/path', ['a', 'b', 'c'], ['e', 'd', 'c'], False,
        )

        assert result is True
        client.put.assert_has_calls([
            mocker.call('/path/groups/d', None),
            mocker.call('/path/groups/e', None),
        ], any_order=True)
        client.delete.assert_has_calls([
            mocker.call('/path/groups/a'),
            mocker.call('/path/groups/b'),
        ], any_order=True)

    def test_update_groups_check_mode(self, mocker):
        client = mocker.Mock()

        result = user.update_groups(
            client, '/path', ['a', 'b', 'c'], ['e', 'd', 'c'], True,
        )

        assert result is True
        client.put.assert_not_called()
        client.delete.assert_not_called()


class TestUpdateState:
    @pytest.mark.parametrize('check', [False, True])
    @pytest.mark.parametrize('state', [False, True])
    def test_update_state_no_change(self, mocker, check, state):
        client = mocker.Mock()

        result = user.update_state(client, '/path', state, state, check)

        assert result is False
        client.put.assert_not_called()
        client.delete.assert_not_called()

    def test_disable_user(self, mocker):
        client = mocker.Mock()
        client.delete.return_value = http.Response(204, '')

        # Go from disabled == False to disabled == True
        result = user.update_state(client, '/path', False, True, False)

        assert result is True
        client.put.assert_not_called()
        client.delete.assert_called_once_with('/path')

    def test_disable_user_check_mode(self, mocker):
        client = mocker.Mock()

        # Go from disabled == False to disabled == True
        result = user.update_state(client, '/path', False, True, True)

        assert result is True
        client.put.assert_not_called()
        client.delete.assert_not_called()

    def test_enable_user(self, mocker):
        client = mocker.Mock()
        client.put.return_value = http.Response(201, '')

        # Go from disabled == True to disabled == False
        result = user.update_state(client, '/path', True, False, False)

        assert result is True
        client.put.assert_called_once_with('/path/reinstate', None)
        client.delete.assert_not_called()

    def test_enable_user_check_mode(self, mocker):
        client = mocker.Mock()

        # Go from disabled == True to disabled == False
        result = user.update_state(client, '/path', True, False, True)

        assert result is True
        client.put.assert_not_called()
        client.delete.assert_not_called()


class TestSync:
    def test_no_current_object(self, mocker):
        client = mocker.Mock()
        client.get.return_value = http.Response(200, '{"new": "data"}')
        client.put.return_value = http.Response(201, '')

        changed, result = user.sync(
            None, client, '/path', {'password': 'data'}, False
        )

        assert changed is True
        assert {'new': 'data'} == result
        client.put.assert_called_once_with('/path', {'password': 'data'})

    def test_no_current_object_check(self, mocker):
        client = mocker.Mock()
        client.get.return_value = http.Response(200, '{"new": "data"}')

        changed, result = user.sync(
            None, client, '/path', {'password_hash': 'data'}, True
        )

        assert changed is True
        assert {} == result
        client.put.assert_not_called()

    def test_password_update(self, mocker):
        client = mocker.Mock()
        client.get.return_value = http.Response(200, '{"new": "data"}')
        p_mock = mocker.patch.object(user, 'update_password')
        p_mock.return_value = True
        g_mock = mocker.patch.object(user, 'update_groups')
        s_mock = mocker.patch.object(user, 'update_state')

        changed, result = user.sync(
            dict(old='data'), client, '/path',
            dict(username='user', password='pass'), False
        )

        assert changed is True
        assert dict(new='data') == result
        p_mock.assert_called_once()
        g_mock.assert_not_called()
        s_mock.assert_not_called()

    def test_password_update_check_mode(self, mocker):
        client = mocker.Mock()
        client.get.return_value = http.Response(200, '{"new": "data"}')
        p_mock = mocker.patch.object(user, 'update_password')
        p_mock.return_value = False
        g_mock = mocker.patch.object(user, 'update_groups')
        s_mock = mocker.patch.object(user, 'update_state')

        changed, result = user.sync(
            dict(old='data'), client, '/path',
            dict(username='user', password='pass'), True
        )

        assert changed is False
        assert dict(old='data', username='user') == result
        p_mock.assert_called_once()
        g_mock.assert_not_called()
        s_mock.assert_not_called()

    def test_password_hash_update(self, mocker):
        client = mocker.Mock()
        client.get.return_value = http.Response(200, '{"new": "data"}')
        mock = mocker.patch.object(user, 'update_password_hash')
        mock.return_value = True

        changed, result = user.sync(
            dict(old='data'), client, '/path',
            dict(username='user', password_hash='pass'), False
        )

        assert changed is True
        assert dict(new='data') == result
        mock.assert_called_once()

    def test_password_hash_update_check_mode(self, mocker):
        client = mocker.Mock()
        client.get.return_value = http.Response(200, '{"new": "data"}')
        mock = mocker.patch.object(user, 'update_password_hash')
        mock.return_value = True

        changed, result = user.sync(
            dict(old='data'), client, '/path',
            dict(username='user', password_hash='pass'), True
        )

        assert changed is True
        assert dict(old='data', username='user') == result
        mock.assert_called_once()

    def test_when_password_is_set_we_ignore_hash(self, mocker):
        client = mocker.Mock()
        client.get.return_value = http.Response(200, '{"new": "data"}')
        p_mock = mocker.patch.object(user, 'update_password')
        p_mock.return_value = True
        h_mock = mocker.patch.object(user, 'update_password_hash')

        user.sync(
            dict(old='data'), client, '/path',
            dict(username='user', password='pass', password_hash='hash'),
            False
        )

        p_mock.assert_called_once()
        h_mock.assert_not_called()

    def test_groups_update(self, mocker):
        client = mocker.Mock()
        client.get.return_value = http.Response(200, '{"new": "data"}')
        p_mock = mocker.patch.object(user, 'update_password')
        g_mock = mocker.patch.object(user, 'update_groups')
        g_mock.return_value = False
        s_mock = mocker.patch.object(user, 'update_state')

        changed, result = user.sync(
            dict(groups=['a']), client, '/path', dict(groups=['b']), False
        )

        assert changed is False
        assert dict(new='data') == result
        p_mock.assert_not_called()
        g_mock.assert_called_once()
        s_mock.assert_not_called()

    def test_groups_update_check_mode(self, mocker):
        client = mocker.Mock()
        client.get.return_value = http.Response(200, '{"new": "data"}')
        p_mock = mocker.patch.object(user, 'update_password')
        g_mock = mocker.patch.object(user, 'update_groups')
        g_mock.return_value = True
        s_mock = mocker.patch.object(user, 'update_state')

        changed, result = user.sync(
            dict(x=3, groups=['a']), client, '/path', dict(groups=['b']), True
        )

        assert changed is True
        assert dict(x=3, groups=['b']) == result
        p_mock.assert_not_called()
        g_mock.assert_called_once()
        s_mock.assert_not_called()

    def test_state_update(self, mocker):
        client = mocker.Mock()
        client.get.return_value = http.Response(200, '{"new": "data"}')
        p_mock = mocker.patch.object(user, 'update_password')
        g_mock = mocker.patch.object(user, 'update_groups')
        s_mock = mocker.patch.object(user, 'update_state')
        s_mock.return_value = False

        changed, result = user.sync(
            dict(disabled=True), client, '/path', dict(disabled=False), False
        )

        assert changed is False
        assert dict(new='data') == result
        p_mock.assert_not_called()
        g_mock.assert_not_called()
        s_mock.assert_called_once()

    def test_state_update_check_mode(self, mocker):
        client = mocker.Mock()
        client.get.return_value = http.Response(200, '{"new": "data"}')
        p_mock = mocker.patch.object(user, 'update_password')
        g_mock = mocker.patch.object(user, 'update_groups')
        s_mock = mocker.patch.object(user, 'update_state')
        s_mock.return_value = True

        changed, result = user.sync(
            dict(disabled=True), client, '/path', dict(disabled=False), True
        )

        assert changed is True
        assert dict(disabled=False) == result
        p_mock.assert_not_called()
        g_mock.assert_not_called()
        s_mock.assert_called_once()


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

        result, _client, path, payload, check_mode = sync_mock.call_args[0]
        assert path == '/api/core/v2/users/alice'
        assert payload == dict(
            username='alice',
            password='alice!?pass',
            disabled=False
        )
        assert check_mode is False

    def test_minimal_parameters_on_existing_user(self, mocker):
        get_mock = mocker.patch.object(utils, 'get')
        get_mock.return_value = dict(username='alice')
        sync_mock = mocker.patch.object(user, 'sync')
        sync_mock.return_value = True, {}
        set_module_args(name='alice')

        with pytest.raises(AnsibleExitJson):
            user.main()

        result, _client, path, payload, check_mode = sync_mock.call_args[0]
        assert path == '/api/core/v2/users/alice'
        assert payload == dict(username='alice', disabled=False)
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

        result, _client, path, payload, check_mode = sync_mock.call_args[0]
        assert path == '/api/core/v2/users/test_user'
        assert payload == dict(
            username='test_user',
            password='password',
            groups=['dev', 'ops'],
            disabled=True
        )
        assert check_mode is False

    def test_cannot_create_user_without_password(self, mocker):
        get_mock = mocker.patch.object(utils, 'get')
        get_mock.return_value = None
        set_module_args(
            name='test_user',
            state='disabled',
            groups=['dev', 'ops'],
        )

        with pytest.raises(AnsibleFailJson, match='without a password'):
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

    def test_failure_on_initial_get(self, mocker):
        get_mock = mocker.patch.object(utils, 'get')
        get_mock.side_effect = errors.Error('Bad error')
        set_module_args(
            name='test_user',
            password='password'
        )

        with pytest.raises(AnsibleFailJson):
            user.main()

    def test_failure_on_missing_bcrypt_5_21_0_or_newer(self, mocker):
        mocker.patch.object(arguments, 'get_sensu_client').return_value = (
            mocker.MagicMock(version='5.22.3')
        )
        mocker.patch.object(user, 'HAS_BCRYPT', False)
        set_module_args(
            name='test_user',
            password='password'
        )

        with pytest.raises(AnsibleFailJson, match='bcrypt'):
            user.main()
