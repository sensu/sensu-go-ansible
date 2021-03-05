from __future__ import absolute_import, division, print_function
__metaclass__ = type

import sys

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, utils,
)
from ansible_collections.sensu.sensu_go.plugins.modules import cluster_role_binding_info

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestClusterRoleBindingInfo(ModuleTestCase):
    def test_get_all_cluster_role_bindings(self, mocker):
        get_mock = mocker.patch.object(utils, "get")
        get_mock.return_value = [1, 2, 3]
        set_module_args()

        with pytest.raises(AnsibleExitJson) as context:
            cluster_role_binding_info.main()

        _client, path = get_mock.call_args[0]
        assert path == "/api/core/v2/clusterrolebindings"
        assert context.value.args[0]["objects"] == [1, 2, 3]

    def test_get_single_cluster_role_binding(self, mocker):
        get_mock = mocker.patch.object(utils, "get")
        get_mock.return_value = 1
        set_module_args(name="test-cluster-role-binding")

        with pytest.raises(AnsibleExitJson) as context:
            cluster_role_binding_info.main()

        _client, path = get_mock.call_args[0]
        assert path == "/api/core/v2/clusterrolebindings/test-cluster-role-binding"
        assert context.value.args[0]["objects"] == [1]

    def test_missing_single_cluster_role_binding(self, mocker):
        get_mock = mocker.patch.object(utils, "get")
        get_mock.return_value = None
        set_module_args(name="sample-cluster-role-binding")

        with pytest.raises(AnsibleExitJson) as context:
            cluster_role_binding_info.main()

        assert context.value.args[0]["objects"] == []

    def test_failure(self, mocker):
        get_mock = mocker.patch.object(utils, "get")
        get_mock.side_effect = errors.Error("Bad error")
        set_module_args(name="sample-cluster-role-binding")

        with pytest.raises(AnsibleFailJson):
            cluster_role_binding_info.main()
