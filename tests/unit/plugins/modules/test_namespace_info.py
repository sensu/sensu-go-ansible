from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, utils,
)
from ansible_collections.sensu.sensu_go.plugins.modules import namespace_info

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)


class TestNamespaceInfo(ModuleTestCase):
    def test_get_namespaces(self, mocker):
        get_mock = mocker.patch.object(utils, "get")
        get_mock.return_value = [1, 2, 3]
        set_module_args()

        with pytest.raises(AnsibleExitJson) as context:
            namespace_info.main()

        _client, path = get_mock.call_args[0]
        assert path == "/api/core/v2/namespaces"
        assert context.value.args[0]["objects"] == [1, 2, 3]

    def test_failure(self, mocker):
        get_mock = mocker.patch.object(utils, "get")
        get_mock.side_effect = errors.Error("Bad error")
        set_module_args()

        with pytest.raises(AnsibleFailJson):
            namespace_info.main()
