from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, utils,
)
from ansible_collections.sensu.sensu_go.plugins.modules import secrets_provider_info

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)


class TestSecretsProviderInfo(ModuleTestCase):
    def test_get_all_secrets_providers(self, mocker):
        get_mock = mocker.patch.object(utils, "get")
        get_mock.return_value = [dict(spec=1), dict(spec=2)]
        set_module_args()

        with pytest.raises(AnsibleExitJson) as context:
            secrets_provider_info.main()

        _client, path = get_mock.call_args[0]
        assert path == "/api/enterprise/secrets/v1/providers"
        assert context.value.args[0]["objects"] == [1, 2]

    def test_get_single_secrets_provider(self, mocker):
        get_mock = mocker.patch.object(utils, "get")
        get_mock.return_value = dict(spec=4)
        set_module_args(name="sample-secrets-provider")

        with pytest.raises(AnsibleExitJson) as context:
            secrets_provider_info.main()

        _client, path = get_mock.call_args[0]
        assert path == "/api/enterprise/secrets/v1/providers/sample-secrets-provider"
        assert context.value.args[0]["objects"] == [4]

    def test_missing_single_secrets_provider(self, mocker):
        get_mock = mocker.patch.object(utils, "get")
        get_mock.return_value = None
        set_module_args(name="sample-secrets-provider")

        with pytest.raises(AnsibleExitJson) as context:
            secrets_provider_info.main()

        assert context.value.args[0]["objects"] == []

    def test_failure(self, mocker):
        get_mock = mocker.patch.object(utils, "get")
        get_mock.side_effect = errors.Error("Bad error")
        set_module_args(name="sample-secrets-provider")

        with pytest.raises(AnsibleFailJson):
            secrets_provider_info.main()
