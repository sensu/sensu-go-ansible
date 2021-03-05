from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, utils
)
from ansible_collections.sensu.sensu_go.plugins.modules import cluster_role

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)


class TestClusterRole(ModuleTestCase):
    def test_minimal_cluster_role_parameters(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.return_value = True, {}
        set_module_args(
            name='test_cluster_role',
            rules=[
                dict(
                    verbs=[],
                    resources=[]
                ),
            ]
        )

        with pytest.raises(AnsibleExitJson):
            cluster_role.main()

        state, _client, path, payload, check_mode, _compare = sync_mock.call_args[0]
        assert state == 'present'
        assert path == '/api/core/v2/clusterroles/test_cluster_role'
        assert payload == dict(
            rules=[
                dict(
                    verbs=[],
                    resources=[],
                    resource_names=None,
                )
            ],
            metadata=dict(
                name='test_cluster_role',
            ),
        )
        assert check_mode is False

    def test_all_cluster_role_parameters(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.return_value = True, {}
        set_module_args(
            name='test_cluster_role',
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
            cluster_role.main()

        state, _client, path, payload, check_mode, _compare = sync_mock.call_args[0]
        assert state == 'present'
        assert path == '/api/core/v2/clusterroles/test_cluster_role'
        assert payload == dict(
            metadata=dict(
                name='test_cluster_role',
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
            name='test_cluster_role',
            rules=[
                dict(
                    verbs=[],
                    resources=[],
                )
            ],
        )
        with pytest.raises(AnsibleFailJson):
            cluster_role.main()

    def test_failure_invalid_verb(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.side_effect = Exception("Validation should fail but didn't")
        set_module_args(
            name='test_cluster_role',
            rules=[
                dict(
                    verbs=['list', 'invalid'],
                    resources=[],
                ),
            ]
        )

        with pytest.raises(AnsibleFailJson):
            cluster_role.main()
