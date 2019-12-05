from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, utils,
)
from ansible_collections.sensu.sensu_go.plugins.modules import event_info

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)


class TestEventInfo(ModuleTestCase):
    def test_get_all_events(self, mocker):
        get_mock = mocker.patch.object(utils, 'get')
        get_mock.return_value = [1, 2, 3]
        set_module_args(namespace="my")

        with pytest.raises(AnsibleExitJson) as context:
            event_info.main()

        _client, path = get_mock.call_args[0]
        assert path == '/api/core/v2/namespaces/my/events'
        assert context.value.args[0]['objects'] == [1, 2, 3]

    def test_get_events_by_entity(self, mocker):
        get_mock = mocker.patch.object(utils, 'get')
        get_mock.return_value = [1, 2]
        set_module_args(
            entity='simple-entity'
        )

        with pytest.raises(AnsibleExitJson) as context:
            event_info.main()

        _client, path = get_mock.call_args[0]
        assert path == '/api/core/v2/namespaces/default/events/simple-entity'
        assert context.value.args[0]['objects'] == [1, 2]

    def test_get_events_by_check(self, mocker):
        get_mock = mocker.patch.object(utils, 'get')
        get_mock.return_value = [1, 2]
        set_module_args(
            check='simple-check'
        )

        with pytest.raises(AnsibleFailJson,
                           match=r"missing parameter\(s\) required by 'check': entity"):
            event_info.main()

    def test_get_single_event_by_entity_and_check(self, mocker):
        get_mock = mocker.patch.object(utils, 'get')
        get_mock.return_value = 4
        set_module_args(
            entity='simple-entity',
            check='simple-check'
        )

        with pytest.raises(AnsibleExitJson) as context:
            event_info.main()

        _client, path = get_mock.call_args[0]
        assert path == '/api/core/v2/namespaces/default/events/simple-entity/simple-check'
        assert context.value.args[0]['objects'] == [4]

    def test_no_event_by_entity_and_check(self, mocker):
        get_mock = mocker.patch.object(utils, "get")
        get_mock.return_value = None
        set_module_args(
            entity='simple-entity',
            check='simple-check'
        )

        with pytest.raises(AnsibleExitJson) as context:
            event_info.main()

        assert context.value.args[0]["objects"] == []

    def test_failure(self, mocker):
        get_mock = mocker.patch.object(utils, 'get')
        get_mock.side_effect = errors.Error('Bad error')
        set_module_args(entity='simple-entity')

        with pytest.raises(AnsibleFailJson):
            event_info.main()
