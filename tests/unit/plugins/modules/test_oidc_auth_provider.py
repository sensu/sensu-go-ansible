from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors,
    utils,
)
from ansible_collections.sensu.sensu_go.plugins.modules import oidc_auth_provider

from .common.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    ModuleTestCase,
    set_module_args,
)

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestADAutProvider(ModuleTestCase):
    def test_minimal_provider_parameters(self, mocker):
        sync_v1_mock = mocker.patch.object(utils, "sync_v1")
        sync_v1_mock.return_value = True, {}
        set_module_args(
            state="present",
            name="oidc_name",
            additional_scopes=["openid"],
            client_id="a8e43af034e7f2608780",
            client_secret="b63968394be6ed2edb61c93847ee792f31bf6216",
            disable_offline_access=False,
            server="https://oidc.example.com:9031",
            username_claim="email",
        )

        with pytest.raises(AnsibleExitJson):
            oidc_auth_provider.main()

        state, _client, path, payload, check_mode = sync_v1_mock.call_args[
            0
        ]

        assert state == "present"
        assert path == "/api/enterprise/authentication/v2/authproviders/oidc_name"
        assert payload == dict(
            type="oidc",
            api_version="authentication/v2",
            metadata=dict(name="oidc_name"),
            spec=dict(
                additional_scopes=["openid"],
                client_id="a8e43af034e7f2608780",
                client_secret="b63968394be6ed2edb61c93847ee792f31bf6216",
                disable_offline_access=False,
                server="https://oidc.example.com:9031",
                username_claim="email",
            ),
        )

        assert check_mode is False

    def test_all_provider_parameters(self, mocker):
        sync_v1_mock = mocker.patch.object(utils, "sync_v1")
        sync_v1_mock.return_value = True, {}
        set_module_args(
            state="present",
            name="oidc_name",
            additional_scopes=["groups", "email", "username"],
            client_id="a8e43af034e7f2608780",
            client_secret="b63968394be6ed2edb61c93847ee792f31bf6216",
            disable_offline_access=False,
            redirect_uri="http://127.0.0.1:8080/api/enterprise/authentication/v2/oidc/callback",
            server="https://oidc.example.com:9031",
            groups_claim="groups",
            groups_prefix="oidc:",
            username_claim="email",
            username_prefix="oidc:",
        )

        with pytest.raises(AnsibleExitJson):
            oidc_auth_provider.main()

        state, _client, path, payload, check_mode = sync_v1_mock.call_args[
            0
        ]
        assert state == "present"
        assert path == "/api/enterprise/authentication/v2/authproviders/oidc_name"
        assert payload == dict(
            type="oidc",
            api_version="authentication/v2",
            metadata=dict(name="oidc_name"),
            spec=dict(
                additional_scopes=["groups", "email", "username"],
                client_id="a8e43af034e7f2608780",
                client_secret="b63968394be6ed2edb61c93847ee792f31bf6216",
                disable_offline_access=False,
                redirect_uri="http://127.0.0.1:8080/api/enterprise/authentication/v2/oidc/callback",
                server="https://oidc.example.com:9031",
                groups_claim="groups",
                groups_prefix="oidc:",
                username_claim="email",
                username_prefix="oidc:",
            ),
        )
        assert check_mode is False

    def test_failure(self, mocker):
        sync_mock = mocker.patch.object(utils, "sync_v1")
        sync_mock.side_effect = errors.Error("Bad error")
        set_module_args()

        with pytest.raises(AnsibleFailJson):
            oidc_auth_provider.main()
