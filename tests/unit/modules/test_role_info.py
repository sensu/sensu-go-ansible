from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, utils,
)
from ansible_collections.sensu.sensu_go.plugins.modules import role_info

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)


class TestRoleInfo(ModuleTestCase):
    def test_get_all_roles(self, mocker):
        get_mock = mocker.patch.object(utils, "get")
        get_mock.return_value = [1, 2, 3]
        set_module_args(namespace="my")

        with pytest.raises(AnsibleExitJson) as context:
            role_info.main()

        _client, path = get_mock.call_args[0]
        assert path == "/api/core/v2/namespaces/my/roles"
        assert context.value.args[0]["objects"] == [1, 2, 3]

    def test_get_single_role(self, mocker):
        get_mock = mocker.patch.object(utils, "get")
        get_mock.return_value = 1
        set_module_args(name="test-role")

        with pytest.raises(AnsibleExitJson) as context:
            role_info.main()

        _client, path = get_mock.call_args[0]
        assert path == "/api/core/v2/namespaces/default/roles/test-role"
        assert context.value.args[0]["objects"] == [1]

    def test_missing_single_role(self, mocker):
        get_mock = mocker.patch.object(utils, "get")
        get_mock.return_value = None
        set_module_args(name="sample-role")

        with pytest.raises(AnsibleExitJson) as context:
            role_info.main()

        assert context.value.args[0]["objects"] == []

    def test_failure(self, mocker):
        get_mock = mocker.patch.object(utils, "get")
        get_mock.side_effect = errors.Error("Bad error")
        set_module_args(name="sample-role")

        with pytest.raises(AnsibleFailJson):
            role_info.main()
