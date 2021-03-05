from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, utils,
)
from ansible_collections.sensu.sensu_go.plugins.modules import secrets_provider_env

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)


class TestSecretsProviderEnv(ModuleTestCase):
    def test_no_provider_parameters(self, mocker):
        sync_v1_mock = mocker.patch.object(utils, 'sync_v1')
        sync_v1_mock.return_value = True, {}
        set_module_args()

        with pytest.raises(AnsibleExitJson):
            secrets_provider_env.main()

        state, _client, path, payload, check_mode = sync_v1_mock.call_args[0]
        assert state == 'present'
        assert path == '/api/enterprise/secrets/v1/providers/env'
        assert payload == dict(
            type='Env',
            api_version="secrets/v1",
            metadata=dict(name='env'),
            spec={}
        )
        assert check_mode is False

    def test_all_provider_parameters(self, mocker):
        sync_v1_mock = mocker.patch.object(utils, 'sync_v1')
        sync_v1_mock.return_value = True, {}
        set_module_args(
            state='present',
        )

        with pytest.raises(AnsibleExitJson):
            secrets_provider_env.main()

        state, _client, path, payload, check_mode = sync_v1_mock.call_args[0]
        assert state == 'present'
        assert path == '/api/enterprise/secrets/v1/providers/env'
        assert payload == dict(
            type='Env',
            api_version="secrets/v1",
            metadata=dict(name='env'),
            spec={}
        )
        assert check_mode is False

    def test_failure(self, mocker):
        sync_v1_mock = mocker.patch.object(utils, 'sync_v1')
        sync_v1_mock.side_effect = errors.Error("Bad error")
        set_module_args()

        with pytest.raises(AnsibleFailJson):
            secrets_provider_env.main()
