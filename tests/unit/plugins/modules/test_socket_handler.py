from __future__ import absolute_import, division, print_function
__metaclass__ = type

import sys

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, utils,
)
from ansible_collections.sensu.sensu_go.plugins.modules import socket_handler

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestSocketHandler(ModuleTestCase):
    def test_minimal_socket_handler_parameters(self, mocker):
        sync_mock = mocker.patch.object(utils, "sync")
        sync_mock.return_value = True, {}
        set_module_args(
            name="test_handler",
            type='tcp',
            host='10.0.1.99',
            port=4444
        )

        with pytest.raises(AnsibleExitJson):
            socket_handler.main()

        state, _client, path, payload, check_mode = sync_mock.call_args[0]
        assert state == "present"
        assert path == "/api/core/v2/namespaces/default/handlers/test_handler"
        assert payload == dict(
            type='tcp',
            socket=dict(
                host='10.0.1.99',
                port=4444
            ),
            metadata=dict(
                name="test_handler",
                namespace="default",
            ),
        )
        assert check_mode is False

    def test_all_socket_handler_parameters(self, mocker):
        sync_mock = mocker.patch.object(utils, "sync")
        sync_mock.return_value = True, {}
        set_module_args(
            name='test_handler',
            namespace='my',
            state='absent',
            type='udp',
            filters=['occurrences', 'production'],
            mutator='only_check_output',
            timeout=30,
            host='10.0.1.99',
            port=4444
        )

        with pytest.raises(AnsibleExitJson):
            socket_handler.main()

        state, _client, path, payload, check_mode = sync_mock.call_args[0]
        assert state == "absent"
        assert path == "/api/core/v2/namespaces/my/handlers/test_handler"
        assert payload == dict(
            type='udp',
            filters=['occurrences', 'production'],
            mutator='only_check_output',
            timeout=30,
            socket=dict(
                host='10.0.1.99',
                port=4444
            ),
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
            type='udp',
            host='10.0.1.99',
            port=4444
        )

        with pytest.raises(AnsibleFailJson):
            socket_handler.main()
