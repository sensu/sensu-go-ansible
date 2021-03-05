from __future__ import absolute_import, division, print_function
__metaclass__ = type

import sys

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, utils,
)
from ansible_collections.sensu.sensu_go.plugins.modules import role

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestRole(ModuleTestCase):
    def test_minimal_role_parameters(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.return_value = True, {}
        set_module_args(
            name='test_role',
            rules=[
                dict(
                    verbs=[],
                    resources=[]
                ),
            ]
        )

        with pytest.raises(AnsibleExitJson):
            role.main()

        state, _client, path, payload, check_mode, _compare = sync_mock.call_args[0]
        assert state == 'present'
        assert path == '/api/core/v2/namespaces/default/roles/test_role'
        assert payload == dict(
            rules=[
                dict(
                    verbs=[],
                    resources=[],
                    resource_names=None,
                )
            ],
            metadata=dict(
                name='test_role',
                namespace='default',
            ),
        )
        assert check_mode is False

    def test_all_role_parameters(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.return_value = True, {}
        set_module_args(
            name='test_role',
            namespace='my',
            state='present',
            rules=[
                dict(
                    verbs=['get', 'list', 'create'],
                    resources=['assets', 'entities'],
                ),
                dict(
                    verbs=['list'],
                    resources=['check'],
                    resource_names=['my-check'],
                )
            ],
        )

        with pytest.raises(AnsibleExitJson):
            role.main()

        state, _client, path, payload, check_mode, _compare = sync_mock.call_args[0]
        assert state == 'present'
        assert path == '/api/core/v2/namespaces/my/roles/test_role'
        assert payload == dict(
            metadata=dict(
                name='test_role',
                namespace='my',
            ),
            rules=[
                dict(
                    verbs=['get', 'list', 'create'],
                    resources=['assets', 'entities'],
                    resource_names=None,
                ),
                dict(
                    verbs=['list'],
                    resources=['check'],
                    resource_names=['my-check'],
                )
            ],
        )

    def test_failure(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.side_effect = errors.Error("Bad error")
        set_module_args(
            name='test_role',
            rules=[
                dict(
                    verbs=[],
                    resources=[],
                )
            ],
        )
        with pytest.raises(AnsibleFailJson):
            role.main()

    def test_failure_invalid_verb(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.side_effect = Exception("Validation should fail but didn't")
        set_module_args(
            name='test_role',
            rules=[
                dict(
                    verbs=['list', 'invalid'],
                    resources=[],
                ),
            ]
        )

        with pytest.raises(AnsibleFailJson):
            role.main()

    def test_failure_empty_rules(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.side_effect = Exception("Validation should fail but didn't")
        set_module_args(
            name='test_role',
            rules=[]
        )

        with pytest.raises(AnsibleFailJson):
            role.main()
