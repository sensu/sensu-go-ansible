from __future__ import absolute_import, division, print_function
__metaclass__ = type

import sys

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, utils,
)
from ansible_collections.sensu.sensu_go.plugins.modules import cluster_role_binding

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestClusterRoleBinding(ModuleTestCase):
    def test_minimal_cluster_role_binding_parameters_users(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.return_value = True, {}
        set_module_args(
            name='test_cluster_role_binding',
            cluster_role='test_cluster_role',
            users=['test_user'],
        )

        with pytest.raises(AnsibleExitJson):
            cluster_role_binding.main()

        state, _client, path, payload, check_mode, _compare = sync_mock.call_args[0]
        assert state == 'present'
        assert path == '/api/core/v2/clusterrolebindings/test_cluster_role_binding'
        assert payload == dict(
            role_ref=dict(
                name='test_cluster_role',
                type='ClusterRole',
            ),
            subjects=[
                dict(
                    name='test_user',
                    type='User',
                ),
            ],
            metadata=dict(
                name='test_cluster_role_binding',
            ),
        )
        assert check_mode is False

    def test_minimal_cluster_role_binding_parameters_groups(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.return_value = True, {}
        set_module_args(
            name='test_cluster_role_binding',
            cluster_role='test_cluster_role',
            groups=['test_group'],
        )

        with pytest.raises(AnsibleExitJson):
            cluster_role_binding.main()

        state, _client, path, payload, check_mode, _compare = sync_mock.call_args[0]
        assert state == 'present'
        assert path == '/api/core/v2/clusterrolebindings/test_cluster_role_binding'
        assert payload == dict(
            role_ref=dict(
                name='test_cluster_role',
                type='ClusterRole',
            ),
            subjects=[
                dict(
                    name='test_group',
                    type='Group',
                ),
            ],
            metadata=dict(
                name='test_cluster_role_binding',
            ),
        )
        assert check_mode is False

    def test_all_cluster_role_binding_parameters(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.return_value = True, {}
        set_module_args(
            name='test_cluster_role_binding',
            cluster_role='test_cluster_role',
            users=['user_1', 'user_2'],
            groups=['group_1', 'group_2'],
        )

        with pytest.raises(AnsibleExitJson):
            cluster_role_binding.main()

        state, _client, path, payload, check_mode, _compare = sync_mock.call_args[0]
        assert state == 'present'
        assert path == '/api/core/v2/clusterrolebindings/test_cluster_role_binding'
        assert payload == dict(
            metadata=dict(
                name='test_cluster_role_binding',
            ),
            role_ref=dict(
                name='test_cluster_role',
                type='ClusterRole',
            ),
            subjects=[
                dict(
                    name='group_1',
                    type='Group',
                ),
                dict(
                    name='group_2',
                    type='Group',
                ),
                dict(
                    name='user_1',
                    type='User',
                ),
                dict(
                    name='user_2',
                    type='User',
                ),
            ]
        )
        assert check_mode is False

    def test_failure(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.side_effect = errors.Error('Bad error')
        set_module_args(
            name='test_cluster_role_binding',
            cluster_role='test_cluster_role',
            users=['test_user'],
        )
        with pytest.raises(AnsibleFailJson):
            cluster_role_binding.main()

    def test_failure_missing_groups_or_users(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.side_effect = Exception("Validation should fail but didn't")
        set_module_args(
            name='test_cluster_role_binding',
            cluster_role='test_cluster_role',
        )

        with pytest.raises(AnsibleFailJson):
            cluster_role_binding.main()
