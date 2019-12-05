from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, utils,
)
from ansible_collections.sensu.sensu_go.plugins.modules import entity

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)


class TestEntity(ModuleTestCase):
    def test_minimal_entity_parameters(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.return_value = True, {}
        set_module_args(
            name='test_entity',
            entity_class='proxy',
        )

        with pytest.raises(AnsibleExitJson):
            entity.main()

        state, _client, path, payload, check_mode = sync_mock.call_args[0]
        assert state == 'present'
        assert path == '/api/core/v2/namespaces/default/entities/test_entity'
        assert payload == dict(
            entity_class='proxy',
            metadata=dict(
                name='test_entity',
                namespace='default',
            ),
        )
        assert check_mode is False

    def test_all_entity_parameters(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.return_value = True, {}
        set_module_args(
            name='test_entity',
            namespace='my',
            state='absent',
            entity_class='proxy',
            subscriptions=['web', 'prod'],
            system=dict(
                hostname='test-entity',
                os='linux',
                platform='ubuntu',
                network=dict(
                    interfaces=[
                        dict(
                            name='lo',
                            addresses=['127.0.0.1/8', '::1/128']
                        ),
                        dict(
                            name='eth0',
                            mac='52:54:00:20:1b:3c',
                            addresses=['93.184.216.34/24']
                        )
                    ])
            ),
            last_seen=1522798317,
            deregister=True,
            deregistration_handler='email-handler',
            redact=['password', 'pass', 'api_key'],
            user='agent'
        )

        with pytest.raises(AnsibleExitJson):
            entity.main()

        state, _client, path, payload, check_mode = sync_mock.call_args[0]
        assert state == 'absent'
        assert path == '/api/core/v2/namespaces/my/entities/test_entity'
        assert payload == dict(
            entity_class='proxy',
            subscriptions=['web', 'prod'],
            system=dict(
                hostname='test-entity',
                os='linux',
                platform='ubuntu',
                network=dict(
                    interfaces=[
                        dict(
                            name='lo',
                            addresses=['127.0.0.1/8', '::1/128']
                        ),
                        dict(
                            name='eth0',
                            mac='52:54:00:20:1b:3c',
                            addresses=['93.184.216.34/24']
                        )
                    ])
            ),
            last_seen=1522798317,
            deregister=True,
            deregistration=dict(handler='email-handler'),
            redact=['password', 'pass', 'api_key'],
            user='agent',
            metadata=dict(
                name='test_entity',
                namespace='my'
            ),
        )
        assert check_mode is False

    def test_failure(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.side_effect = errors.Error('Bad error')
        set_module_args(
            name='test_entity',
            entity_class='proxy'
        )

        with pytest.raises(AnsibleFailJson):
            entity.main()
