from __future__ import absolute_import, division, print_function
__metaclass__ = type

import sys

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, utils,
)
from ansible_collections.sensu.sensu_go.plugins.modules import auth_provider_info

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestAuthProviderInfo(ModuleTestCase):
    def test_get_all_auth_providers(self, mocker):
        get_mock = mocker.patch.object(utils, "get")
        get_mock.return_value = [dict(spec=dict(a=1)), dict(spec=dict(b=2))]
        set_module_args()

        with pytest.raises(AnsibleExitJson) as context:
            auth_provider_info.main()

        _client, path = get_mock.call_args[0]
        assert path == "/api/enterprise/authentication/v2/authproviders"
        assert context.value.args[0]["objects"] == [dict(a=1), dict(b=2)]

    def test_get_single_auth_provider(self, mocker):
        get_mock = mocker.patch.object(utils, "get")
        get_mock.return_value = dict(spec=dict(a=1))
        set_module_args(name="sample-auth-provider")

        with pytest.raises(AnsibleExitJson) as context:
            auth_provider_info.main()

        _client, path = get_mock.call_args[0]
        assert path == "/api/enterprise/authentication/v2/authproviders/sample-auth-provider"
        assert context.value.args[0]["objects"] == [dict(a=1)]

    def test_missing_single_auth_provider(self, mocker):
        get_mock = mocker.patch.object(utils, "get")
        get_mock.return_value = None
        set_module_args(name="sample-auth-provider")

        with pytest.raises(AnsibleExitJson) as context:
            auth_provider_info.main()

        assert context.value.args[0]["objects"] == []

    def test_failure(self, mocker):
        get_mock = mocker.patch.object(utils, "get")
        get_mock.side_effect = errors.Error("Bad error")
        set_module_args(name="sample-auth-provider")

        with pytest.raises(AnsibleFailJson):
            auth_provider_info.main()
