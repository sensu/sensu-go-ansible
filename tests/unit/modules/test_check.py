from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, utils,
)
from ansible_collections.sensu.sensu_go.plugins.modules import check

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)


class TestSensuGoCheck(ModuleTestCase):
    def test_minimal_check_parameters(self, mocker):
        sync_mock = mocker.patch.object(utils, "sync")
        sync_mock.return_value = True, {}
        set_module_args(
            name="test_check",
            command='echo "test"',
            subscriptions=['switches'],
            interval=60
        )

        with pytest.raises(AnsibleExitJson):
            check.main()

        state, _client, path, payload, check_mode = sync_mock.call_args[0]
        assert state == "present"
        assert path == "/checks/test_check"
        assert payload == dict(
            command='echo "test"',
            subscriptions=['switches'],
            interval=60,
            metadata=dict(
                name="test_check",
                namespace="default",
            ),
        )
        assert check_mode is False

    def test_all_check_parameters(self, mocker):
        sync_mock = mocker.patch.object(utils, "sync")
        sync_mock.return_value = True, {}
        set_module_args(
            name='test_check',
            state='absent',
            command='/bin/true',
            subscriptions=['checks', 'also_checks'],
            handlers=['default', 'not_default'],
            interval=30,
            publish=True,
            timeout=30,
            ttl=100,
            stdin=False,
            low_flap_threshold=20,
            high_flap_threshold=60,
            proxy_entity_name='switch-dc-01',
            proxy_requests=dict(
                entity_attributes=['entity.entity_class == "proxy"'],
                splay=True,
                splay_coverage=90
            ),
            output_metric_format='nagios_perfdata',
            output_metric_handlers=['influx-db'],
            round_robin=True,
            env_vars=dict(foo='bar'),
            runtime_assets='awesomeness'
        )

        with pytest.raises(AnsibleExitJson):
            check.main()

        state, _client, path, payload, check_mode = sync_mock.call_args[0]
        assert state == "absent"
        assert path == "/checks/test_check"
        assert payload == dict(
            command='/bin/true',
            subscriptions=['checks', 'also_checks'],
            interval=30,
            timeout=30,
            publish=True,
            handlers=['default', 'not_default'],
            env_vars=['foo=bar'],
            output_metric_handlers=['influx-db'],
            ttl=100,
            output_metric_format='nagios_perfdata',
            proxy_entity_name='switch-dc-01',
            proxy_requests=dict(entity_attributes=['entity.entity_class == "proxy"'],
                                splay=True,
                                splay_coverage=90),
            high_flap_threshold=60,
            low_flap_threshold=20,
            round_robin=True,
            stdin=False,
            runtime_assets=['awesomeness'],
            metadata=dict(
                name="test_check",
                namespace="default",
            ),
        )
        assert check_mode is False

    def test_failure(self, mocker):
        sync_mock = mocker.patch.object(utils, "sync")
        sync_mock.side_effect = errors.Error("Bad error")
        set_module_args(
            name='test_check',
            command='/bin/true',
            subscriptions=['checks', 'also_checks'],
            handlers=['default', 'not_default'],
            interval=30,
            publish=True,
            timeout=30,
            ttl=100,
            stdin=False,
            low_flap_threshold=20,
            high_flap_threshold=60,
            proxy_entity_name='switch-dc-01',
            proxy_requests=dict(
                entity_attributes=['entity.entity_class == "proxy"'],
                splay=True,
                splay_coverage=90
            ),
            output_metric_format='nagios_perfdata',
            output_metric_handlers=['influx-db'],
            round_robin=True,
            env_vars=dict(foo='bar'),
            runtime_assets='awesomeness'
        )

        with pytest.raises(AnsibleFailJson):
            check.main()
