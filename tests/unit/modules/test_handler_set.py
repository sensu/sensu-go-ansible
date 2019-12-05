from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, utils,
)
from ansible_collections.sensu.sensu_go.plugins.modules import handler_set

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)


class TestHandlerSet(ModuleTestCase):
    def test_all_handler_set_parameters(self, mocker):
        sync_mock = mocker.patch.object(utils, "sync")
        sync_mock.return_value = True, {}
        set_module_args(
            name='test_handler',
            namespace='my',
            state='absent',
            handlers=['tcp_handler', 'udp_handler']
        )

        with pytest.raises(AnsibleExitJson):
            handler_set.main()

        state, _client, path, payload, check_mode = sync_mock.call_args[0]
        assert state == "absent"
        assert path == "/api/core/v2/namespaces/my/handlers/test_handler"
        assert payload == dict(
            type='set',
            handlers=['tcp_handler', 'udp_handler'],
            metadata=dict(
                name="test_handler",
                namespace="my",
            ),
        )
        assert check_mode is False

    def test_failure(self, mocker):
        sync_mock = mocker.patch.object(utils, "sync")
        sync_mock.side_effect = errors.Error("Bad error")
        set_module_args(
            name='test_handler',
            state='absent',
            handlers=['tcp_handler', 'udp_handler']
        )

        with pytest.raises(AnsibleFailJson):
            handler_set.main()
