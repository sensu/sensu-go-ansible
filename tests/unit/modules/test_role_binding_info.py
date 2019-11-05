from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, utils,
)
from ansible_collections.sensu.sensu_go.plugins.modules import role_binding_info

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)


class TestRoleBindingInfo(ModuleTestCase):
    def test_get_all_role_bindings(self, mocker):
        get_mock = mocker.patch.object(utils, "get")
        get_mock.return_value = [1, 2, 3]
        set_module_args()

        with pytest.raises(AnsibleExitJson) as context:
            role_binding_info.main()

        _client, path = get_mock.call_args[0]
        assert path == "/rolebindings"
        assert context.value.args[0]["objects"] == [1, 2, 3]

    def test_get_single_role_binding(self, mocker):
        get_mock = mocker.patch.object(utils, "get")
        get_mock.return_value = 1
        set_module_args(name="test-role-binding")

        with pytest.raises(AnsibleExitJson) as context:
            role_binding_info.main()

        _client, path = get_mock.call_args[0]
        assert path == "/rolebindings/test-role-binding"
        assert context.value.args[0]["objects"] == [1]

    def test_failure(self, mocker):
        get_mock = mocker.patch.object(utils, "get")
        get_mock.side_effect = errors.Error("Bad error")
        set_module_args(name="sample-role-binding")

        with pytest.raises(AnsibleFailJson):
            role_binding_info.main()
