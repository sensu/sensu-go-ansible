from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, utils,
)
from ansible_collections.sensu.sensu_go.plugins.modules import mutator

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)


class TestMutator(ModuleTestCase):
    def test_minimal_mutator_parameters(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.return_value = True, {}
        set_module_args(
            name='test_mutator',
            command='/bin/true',
        )

        with pytest.raises(AnsibleExitJson):
            mutator.main()

        state, _client, path, payload, check_mode = sync_mock.call_args[0]
        assert state == 'present'
        assert path == '/api/core/v2/namespaces/default/mutators/test_mutator'
        assert payload == dict(
            command='/bin/true',
            metadata=dict(
                name='test_mutator',
                namespace='default',
            ),
        )
        assert check_mode is False

    def test_all_mutator_parameters(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.return_value = True, {}
        set_module_args(
            name='test_mutator',
            namespace='my',
            state='absent',
            command='/bin/true',
            timeout=30,
            runtime_assets='awesomeness',
            labels={'region': 'us-west-1'},
            annotations={'playbook': 12345},
        )

        with pytest.raises(AnsibleExitJson):
            mutator.main()

        state, _client, path, payload, check_mode = sync_mock.call_args[0]
        assert state == 'absent'
        assert path == '/api/core/v2/namespaces/my/mutators/test_mutator'
        assert payload == dict(
            command='/bin/true',
            timeout=30,
            runtime_assets=['awesomeness'],
            metadata=dict(
                name='test_mutator',
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
            name='test_mutator',
            command='/bion/true'
        )

        with pytest.raises(AnsibleFailJson):
            mutator.main()
