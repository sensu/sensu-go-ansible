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
        set_module_args()

        with pytest.raises(AnsibleExitJson) as context:
            event_info.main()

        _client, path = get_mock.call_args[0]
        assert path == '/events'
        assert context.value.args[0]['objects'] == [1, 2, 3]

    def test_get_events_by_entity_name(self, mocker):
        get_mock = mocker.patch.object(utils, 'get')
        get_mock.return_value = [1, 2]
        set_module_args(
            entity_name='sample-entity'
        )

        with pytest.raises(AnsibleExitJson) as context:
            event_info.main()

        _client, path = get_mock.call_args[0]
        assert path == '/events/sample-entity'
        assert context.value.args[0]['objects'] == [1, 2]

    def test_get_single_event_by_entity_and_check_name(self, mocker):
        get_mock = mocker.patch.object(utils, 'get')
        get_mock.return_value = 4
        set_module_args(
            entity_name='sample-entity',
            check_name='sample-check'
        )

        with pytest.raises(AnsibleExitJson) as context:
            event_info.main()

        _client, path = get_mock.call_args[0]
        assert path == '/events/sample-entity/sample-check'
        assert context.value.args[0]['objects'] == [4]

    def test_failure(self, mocker):
        get_mock = mocker.patch.object(utils, 'get')
        get_mock.side_effect = errors.Error('Bad error')
        set_module_args(entity_name='sample-entity')

        with pytest.raises(AnsibleFailJson):
            event_info.main()
