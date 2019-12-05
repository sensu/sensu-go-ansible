from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, utils,
)
from ansible_collections.sensu.sensu_go.plugins.modules import hook

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)


class TestHook(ModuleTestCase):
    def test_minimal_hook_parameters(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.return_value = True, {}
        set_module_args(
            name='test_hook',
            command='/bin/true',
            timeout=10,
        )

        with pytest.raises(AnsibleExitJson):
            hook.main()

        state, _client, path, payload, check_mode = sync_mock.call_args[0]
        assert state == 'present'
        assert path == '/api/core/v2/namespaces/default/hooks/test_hook'
        assert payload == dict(
            command='/bin/true',
            timeout=10,
            metadata=dict(
                name='test_hook',
                namespace='default',
            ),
        )
        assert check_mode is False

    def test_all_hook_parameters(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.return_value = True, {}
        set_module_args(
            name='test_hook',
            namespace='my',
            state='absent',
            command='/bin/true',
            timeout=30,
            stdin=True,
            runtime_assets='awesomeness',
            labels={'region': 'us-west-1'},
            annotations={'playbook': 12345},
        )

        with pytest.raises(AnsibleExitJson):
            hook.main()

        state, _client, path, payload, check_mode = sync_mock.call_args[0]
        assert state == 'absent'
        assert path == '/api/core/v2/namespaces/my/hooks/test_hook'
        assert payload == dict(
            command='/bin/true',
            timeout=30,
            stdin=True,
            runtime_assets=['awesomeness'],
            metadata=dict(
                name='test_hook',
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
            name='test_hook',
            command='/bin/true',
            timeout=10
        )

        with pytest.raises(AnsibleFailJson):
            hook.main()
