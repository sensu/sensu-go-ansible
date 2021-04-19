from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors,
    utils,
)
from ansible_collections.sensu.sensu_go.plugins.modules import ldap_auth_provider

from .common.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    ModuleTestCase,
    set_module_args,
)

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestDoDiffer:
    def test_no_changes(self):
        desired = dict(
            spec=dict(
                servers=[
                    dict(
                        host="127.0.0.1",
                        group_search=dict(
                            base_dn="dc=acme,dc=org",
                        ),
                        user_search=dict(
                            base_dn="dc=acme,dc=org",
                        ),
                    )
                ],
            ),
            metadata=dict(name="openldap"),
        )
        current = dict(
            spec=dict(
                servers=[
                    dict(
                        host="127.0.0.1",
                        group_search=dict(
                            base_dn="dc=acme,dc=org",
                        ),
                        user_search=dict(
                            base_dn="dc=acme,dc=org",
                        ),
                    )
                ],
            ),
            metadata=dict(
                name="openldap",
                created_by="me",
            ),
        )

        assert ldap_auth_provider.do_differ(current, desired) is False

    def test_changes_are_detected(self):
        desired = dict(
            spec=dict(
                servers=[
                    dict(
                        host="127.0.0.1",
                        port=636,
                        group_search=dict(
                            base_dn="dc=acme,dc=org",
                        ),
                        user_search=dict(
                            base_dn="dc=acme,dc=org",
                        ),
                    )
                ],
            ),
            metadata=dict(name="openldap"),
        )
        current = dict(
            spec=dict(
                servers=[
                    dict(
                        host="127.0.0.1",
                        group_search=dict(
                            base_dn="dc=acme,dc=org",
                        ),
                        user_search=dict(
                            base_dn="dc=acme,dc=org",
                        ),
                    )
                ],
            ),
            metadata=dict(
                name="openldap",
                created_by="me",
            ),
        )
        assert ldap_auth_provider.do_differ(current, desired) is True

    def test_changes_are_detected_diff_servers_len(self):
        desired = dict(
            spec=dict(
                servers=[
                    dict(
                        host="127.0.0.1",
                        group_search=dict(
                            base_dn="dc=acme,dc=org",
                        ),
                        user_search=dict(
                            base_dn="dc=acme,dc=org",
                        ),
                    ),
                    dict(
                        host="127.0.0.2",
                        group_search=dict(
                            base_dn="dc=acme,dc=org",
                        ),
                        user_search=dict(
                            base_dn="dc=acme,dc=org",
                        ),
                    ),
                ],
            ),
            metadata=dict(name="openldap"),
        )
        current = dict(
            spec=dict(
                servers=[
                    dict(
                        host="127.0.0.1",
                        group_search=dict(
                            base_dn="dc=acme,dc=org",
                        ),
                        user_search=dict(
                            base_dn="dc=acme,dc=org",
                        ),
                    )
                ],
            ),
            metadata=dict(
                name="openldap",
                created_by="me",
            ),
        )
        assert ldap_auth_provider.do_differ(current, desired) is True

    def test_changes_are_other_params(self):
        desired = dict(
            spec=dict(
                servers=[],
                groups_prefix="ldap",
                username_prefix="ldap",
            ),
            metadata=dict(name="openldap"),
        )
        current = dict(
            spec=dict(
                servers=[],
            ),
            metadata=dict(
                name="openldap",
                created_by="me",
            ),
        )
        assert ldap_auth_provider.do_differ(current, desired) is True


class TestLDAPAutProvider(ModuleTestCase):
    def test_minimal_provider_parameters(self, mocker):
        sync_v1_mock = mocker.patch.object(utils, "sync_v1")
        sync_v1_mock.return_value = True, {}
        set_module_args(
            state="present",
            name="openldap",
            servers=[
                dict(
                    host="127.0.0.1",
                    group_search=dict(
                        base_dn="dc=acme,dc=org",
                    ),
                    user_search=dict(
                        base_dn="dc=acme,dc=org",
                    ),
                )
            ],
        )

        with pytest.raises(AnsibleExitJson):
            ldap_auth_provider.main()

        state, _client, path, payload, check_mode, _do_differ = sync_v1_mock.call_args[
            0
        ]

        assert state == "present"
        assert path == "/api/enterprise/authentication/v2/authproviders/openldap"
        assert payload == dict(
            type="ldap",
            api_version="authentication/v2",
            metadata=dict(name="openldap"),
            spec=dict(
                servers=[
                    dict(
                        host="127.0.0.1",
                        port=None,
                        insecure=False,
                        security="tls",
                        trusted_ca_file=None,
                        client_cert_file=None,
                        client_key_file=None,
                        binding=None,
                        group_search=dict(
                            base_dn="dc=acme,dc=org",
                            attribute="member",
                            name_attribute="cn",
                            object_class="groupOfNames",
                        ),
                        user_search=dict(
                            base_dn="dc=acme,dc=org",
                            attribute="uid",
                            name_attribute="cn",
                            object_class="person",
                        ),
                    )
                ]
            ),
        )

        assert check_mode is False

    def test_all_provider_parameters(self, mocker):
        sync_v1_mock = mocker.patch.object(utils, "sync_v1")
        sync_v1_mock.return_value = True, {}
        set_module_args(
            state="present",
            name="openldap",
            servers=[
                dict(
                    host="127.0.0.1",
                    port=636,
                    insecure=False,
                    security="tls",
                    trusted_ca_file="/path/to/trusted-certificate-authorities.pem",
                    client_cert_file="/path/to/ssl/cert.pem",
                    client_key_file="/path/to/ssl/key.pem",
                    binding=dict(
                        user_dn="cn=binder,dc=acme,dc=org",
                        password="YOUR_PASSWORD",
                    ),
                    group_search=dict(
                        base_dn="dc=acme,dc=org",
                        attribute="member",
                        name_attribute="cn",
                        object_class="groupOfNames",
                    ),
                    user_search=dict(
                        base_dn="dc=acme,dc=org",
                        attribute="uid",
                        name_attribute="cn",
                        object_class="person",
                    ),
                )
            ],
            groups_prefix="ldap",
            username_prefix="ldap",
        )

        with pytest.raises(AnsibleExitJson):
            ldap_auth_provider.main()

        state, _client, path, payload, check_mode, _do_differ = sync_v1_mock.call_args[
            0
        ]
        assert state == "present"
        assert path == "/api/enterprise/authentication/v2/authproviders/openldap"
        assert payload == dict(
            type="ldap",
            api_version="authentication/v2",
            metadata=dict(name="openldap"),
            spec=dict(
                servers=[
                    dict(
                        host="127.0.0.1",
                        port=636,
                        insecure=False,
                        security="tls",
                        trusted_ca_file="/path/to/trusted-certificate-authorities.pem",
                        client_cert_file="/path/to/ssl/cert.pem",
                        client_key_file="/path/to/ssl/key.pem",
                        binding=dict(
                            user_dn="cn=binder,dc=acme,dc=org",
                            password="YOUR_PASSWORD",
                        ),
                        group_search=dict(
                            base_dn="dc=acme,dc=org",
                            attribute="member",
                            name_attribute="cn",
                            object_class="groupOfNames",
                        ),
                        user_search=dict(
                            base_dn="dc=acme,dc=org",
                            attribute="uid",
                            name_attribute="cn",
                            object_class="person",
                        ),
                    )
                ],
                groups_prefix="ldap",
                username_prefix="ldap",
            ),
        )
        assert check_mode is False

    def test_failure(self, mocker):
        sync_mock = mocker.patch.object(utils, "sync_v1")
        sync_mock.side_effect = errors.Error("Bad error")
        set_module_args()

        with pytest.raises(AnsibleFailJson):
            ldap_auth_provider.main()
