from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, utils,
)
from ansible_collections.sensu.sensu_go.plugins.modules import filter

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)


class TestFilter(ModuleTestCase):
    def test_minimal_filter_parameters(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.return_value = True, {}
        set_module_args(
            name='test_filter',
            action='allow',
            expressions='event.check.occurences == 1',
        )

        with pytest.raises(AnsibleExitJson):
            filter.main()

        state, _client, path, payload, check_mode = sync_mock.call_args[0]
        assert state == 'present'
        assert path == '/api/core/v2/namespaces/default/filters/test_filter'
        assert payload == dict(
            action='allow',
            expressions=['event.check.occurences == 1'],
            metadata=dict(
                name='test_filter',
                namespace='default',
            ),
        )
        assert check_mode is False

    def test_all_filter_parameters(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.return_value = True, {}
        set_module_args(
            name='test_filter',
            namespace='my',
            state='absent',
            action='allow',
            expressions='event.check.occurences == 1',
            runtime_assets='awesomeness',
            labels={'region': 'us-west-1'},
            annotations={'playbook': 12345},
        )

        with pytest.raises(AnsibleExitJson):
            filter.main()

        state, _client, path, payload, check_mode = sync_mock.call_args[0]
        assert state == 'absent'
        assert path == '/api/core/v2/namespaces/my/filters/test_filter'
        assert payload == dict(
            action='allow',
            expressions=['event.check.occurences == 1'],
            runtime_assets=['awesomeness'],
            metadata=dict(
                name='test_filter',
                namespace='my',
                labels={'region': 'us-west-1'},
                annotations={'playbook': '12345'},
            ),
        )
        assert check_mode is False

    def test_failure(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.side_effect = errors.Error('Bad error')
        set_module_args(
            name='test_filter',
            action='deny',
            expressions='event.check.occurences == 1',
        )

        with pytest.raises(AnsibleFailJson):
            filter.main()
