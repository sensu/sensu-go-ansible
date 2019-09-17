from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, utils,
)
from ansible_collections.sensu.sensu_go.plugins.modules import pipe_handler

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)


class TestPipeHandler(ModuleTestCase):
    def test_minimal_pipe_handler_parameters(self, mocker):
        sync_mock = mocker.patch.object(utils, "sync")
        sync_mock.return_value = True, {}
        set_module_args(
            name="test_handler",
            command='echo "test"'
        )

        with pytest.raises(AnsibleExitJson):
            pipe_handler.main()

        state, _client, path, payload, check_mode = sync_mock.call_args[0]
        assert state == "present"
        assert path == "/handlers/test_handler"
        assert payload == dict(
            command='echo "test"',
            type='pipe',
            metadata=dict(
                name="test_handler",
                namespace="default",
            ),
        )
        assert check_mode is False

    def test_all_pipe_handler_parameters(self, mocker):
        sync_mock = mocker.patch.object(utils, "sync")
        sync_mock.return_value = True, {}
        set_module_args(
            name='test_handler',
            state='absent',
            command='/bin/true',
            filters=['occurrences', 'production'],
            mutator='only_check_output',
            timeout=30,
            env_vars=dict(foo='bar'),
            runtime_assets='awesomeness'
        )

        with pytest.raises(AnsibleExitJson):
            pipe_handler.main()

        state, _client, path, payload, check_mode = sync_mock.call_args[0]
        assert state == "absent"
        assert path == "/handlers/test_handler"
        assert payload == dict(
            command='/bin/true',
            type='pipe',
            filters=['occurrences', 'production'],
            mutator='only_check_output',
            timeout=30,
            env_vars=['foo=bar'],
            runtime_assets=['awesomeness'],
            metadata=dict(
                name="test_handler",
                namespace="default",
            ),
        )
        assert check_mode is False

    def test_failure(self, mocker):
        sync_mock = mocker.patch.object(utils, "sync")
        sync_mock.side_effect = errors.Error("Bad error")
        set_module_args(
            name='test_handler',
            state='absent',
            command='/bin/true',
            filters=['occurrences', 'production'],
            mutator='only_check_output',
            timeout=30,
            env_vars=dict(foo='bar'),
            runtime_assets='awesomeness'
        )

        with pytest.raises(AnsibleFailJson):
            pipe_handler.main()
