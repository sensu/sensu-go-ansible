from __future__ import absolute_import, division, print_function
__metaclass__ = type

import sys

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, utils,
)
from ansible_collections.sensu.sensu_go.plugins.modules import secrets_provider_vault

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestDoDiffer:
    def test_fields_are_ignored(self):
        desired = dict(
            spec=dict(
                client=dict(
                    address="https://my-vault.com",
                    tls=dict(
                        ca_cert="cert"
                    ),
                ),
            ),
            metadata=dict(
                name="my-vault"
            )
        )
        current = dict(
            spec=dict(
                client=dict(
                    address="https://my-vault.com",
                    agent_address="",  # extra field
                    tls=dict(
                        ca_cert="cert",
                        # extra fields
                        insecure=False,
                        ca_path="path",
                        tls_server_name="server",
                    )
                ),
            ),
            metadata=dict(
                name="my-vault",
                created_by="me",
            )
        )

        assert secrets_provider_vault.do_differ(current, desired) is False

    def test_changes_are_detected(self):
        desired = dict(
            spec=dict(
                client=dict(
                    address="https://my-vault.com",
                    tls=dict(
                        ca_cert="cert"
                    ),
                ),
            ),
            metadata=dict(
                name="my-vault"
            )
        )
        current = dict(
            spec=dict(
                client=dict(
                    address="https://my-vault.com",
                    tls=dict(
                        ca_cert="new-cert",
                        cname="server",
                    ),
                    timeout='15s',
                ),
            ),
            metadata=dict(
                name="my-vault",
            )
        )
        assert secrets_provider_vault.do_differ(current, desired) is True


class TestSecretsProviderVault(ModuleTestCase):
    def test_minimal_provider_parameters(self, mocker):
        sync_v1_mock = mocker.patch.object(utils, 'sync_v1')
        sync_v1_mock.return_value = True, {}
        set_module_args(
            name='my-vault',
            state='present',
            address='https://my-vault.com',
            token='AUTH_TOKEN',
            version='v1',
        )

        with pytest.raises(AnsibleExitJson):
            secrets_provider_vault.main()

        state, _client, path, payload, check_mode, _do_differ = sync_v1_mock.call_args[0]
        assert state == 'present'
        assert path == '/api/enterprise/secrets/v1/providers/my-vault'
        assert payload == dict(
            type='VaultProvider',
            api_version="secrets/v1",
            metadata=dict(name='my-vault'),
            spec=dict(
                client=dict(
                    address='https://my-vault.com',
                    token='AUTH_TOKEN',
                    version='v1',
                ),
            ),
        )
        assert check_mode is False

    def test_all_provider_parameters(self, mocker):
        sync_v1_mock = mocker.patch.object(utils, 'sync_v1')
        sync_v1_mock.return_value = True, {}
        set_module_args(
            name='my-vault',
            state='present',
            address='https://my-vault.com',
            token='AUTH_TOKEN',
            version='v1',
            tls=dict(
                ca_cert='/etc/ssl/ca.crt',
                client_cert='/etc/ssl/client.crt',
                client_key='/etc/ssl/client.key',
                cname='my-vault.com',
            ),
            timeout=1,
            max_retries=2,
            rate_limit=3,
            burst_limit=4,
        )

        with pytest.raises(AnsibleExitJson):
            secrets_provider_vault.main()

        state, _client, path, payload, check_mode, _do_differ = sync_v1_mock.call_args[0]
        assert state == 'present'
        assert path == '/api/enterprise/secrets/v1/providers/my-vault'
        assert payload == dict(
            type='VaultProvider',
            api_version="secrets/v1",
            metadata=dict(name='my-vault'),
            spec=dict(
                client=dict(
                    address='https://my-vault.com',
                    token='AUTH_TOKEN',
                    version='v1',
                    tls=dict(
                        ca_cert='/etc/ssl/ca.crt',
                        client_cert='/etc/ssl/client.crt',
                        client_key='/etc/ssl/client.key',
                        cname='my-vault.com',
                    ),
                    timeout="1s",
                    max_retries=2,
                    rate_limiter=dict(
                        limit=3,
                        burst=4,
                    ),
                ),
            ),
        )
        assert check_mode is False

    def test_failure(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync_v1')
        sync_mock.side_effect = errors.Error("Bad error")
        set_module_args()

        with pytest.raises(AnsibleFailJson):
            secrets_provider_vault.main()
