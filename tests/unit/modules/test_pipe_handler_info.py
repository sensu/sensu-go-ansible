from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, utils,
)
from ansible_collections.sensu.sensu_go.plugins.modules import handler_info

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)


class TestHandlerInfo(ModuleTestCase):
    def test_get_all_handlers(self, mocker):
        get_mock = mocker.patch.object(utils, "get")
        get_mock.return_value = [1, 2, 3]
        set_module_args()

        with pytest.raises(AnsibleExitJson) as context:
            handler_info.main()

        _client, path = get_mock.call_args[0]
        assert path == "/handlers"
        assert context.value.args[0]["objects"] == [1, 2, 3]

    def test_get_single_handler(self, mocker):
        get_mock = mocker.patch.object(utils, "get")
        get_mock.return_value = 4
        set_module_args(name="sample-handler")

        with pytest.raises(AnsibleExitJson) as context:
            handler_info.main()

        _client, path = get_mock.call_args[0]
        assert path == "/handlers/sample-handler"
        assert context.value.args[0]["objects"] == [4]

    def test_missing_single_handler(self, mocker):
        get_mock = mocker.patch.object(utils, "get")
        get_mock.return_value = None
        set_module_args(name="sample-handler")

        with pytest.raises(AnsibleExitJson) as context:
            handler_info.main()

        assert context.value.args[0]["objects"] == []

    def test_failure(self, mocker):
        get_mock = mocker.patch.object(utils, "get")
        get_mock.side_effect = errors.Error("Bad error")
        set_module_args(name="sample-handler")

        with pytest.raises(AnsibleFailJson):
            handler_info.main()
