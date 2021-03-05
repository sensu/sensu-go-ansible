from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, utils,
)
from ansible_collections.sensu.sensu_go.plugins.modules import entity_info

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)


class TestEntityInfo(ModuleTestCase):
    def test_get_all_entities(self, mocker):
        get_mock = mocker.patch.object(utils, "get")
        get_mock.return_value = [1, 2, 3]
        set_module_args(namespace="my")

        with pytest.raises(AnsibleExitJson) as context:
            entity_info.main()

        _client, path = get_mock.call_args[0]
        assert path == "/api/core/v2/namespaces/my/entities"
        assert context.value.args[0]["objects"] == [1, 2, 3]

    def test_get_single_entity(self, mocker):
        get_mock = mocker.patch.object(utils, "get")
        get_mock.return_value = 4
        set_module_args(name="sample-entity")

        with pytest.raises(AnsibleExitJson) as context:
            entity_info.main()

        _client, path = get_mock.call_args[0]
        assert path == "/api/core/v2/namespaces/default/entities/sample-entity"
        assert context.value.args[0]["objects"] == [4]

    def test_missing_single_entity(self, mocker):
        get_mock = mocker.patch.object(utils, "get")
        get_mock.return_value = None
        set_module_args(name="sample-entity")

        with pytest.raises(AnsibleExitJson) as context:
            entity_info.main()

        assert context.value.args[0]["objects"] == []

    def test_failure(self, mocker):
        get_mock = mocker.patch.object(utils, "get")
        get_mock.side_effect = errors.Error("Bad error")
        set_module_args(name="sample-entity")

        with pytest.raises(AnsibleFailJson):
            entity_info.main()
