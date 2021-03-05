from __future__ import absolute_import, division, print_function
__metaclass__ = type

import sys

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, http,
)
from ansible_collections.sensu.sensu_go.plugins.modules import event

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestGetObjects:
    def test_get_entity(self, mocker):
        client = mocker.Mock()
        client.get.return_value = http.Response(200, '{"entity": "entity"}')
        resp = event.get_entity(client, 'default', 'entity')

        assert resp == {'entity': 'entity'}

    def test_get_entity_404(self, mocker):
        client = mocker.Mock()
        client.get.return_value = http.Response(404, '')

        with pytest.raises(errors.SyncError,
                           match="Entity with name 'entity' does not exist on remote."):
            event.get_entity(client, 'default', 'entity')

    def test_get_check(self, mocker):
        client = mocker.Mock()
        client.get.return_value = http.Response(200, '{"check": "check"}')
        resp = event.get_check(client, 'default', 'check')

        assert resp == {'check': 'check'}

    def test_get_check_404(self, mocker):
        client = mocker.Mock()
        client.get.return_value = http.Response(404, '')

        with pytest.raises(errors.SyncError,
                           match="Check with name 'check' does not exist on remote."):
            event.get_check(client, 'default', 'check')


class TestEvent(ModuleTestCase):
    def test_missing_entity_on_remote(self, mocker):
        get_entity_mock = mocker.patch.object(event, 'get_entity')
        get_entity_mock.side_effect = errors.SyncError('Error')

        set_module_args(
            entity='awesome_entity',
            check='awesome_check',
        )

        with pytest.raises(AnsibleFailJson, match='Error'):
            event.main()

    def test_missing_check_on_remote(self, mocker):
        mocker.patch.object(event, 'get_entity')
        get_check_mock = mocker.patch.object(event, 'get_check')
        get_check_mock.side_effect = errors.SyncError('Error')

        set_module_args(
            entity='awesome_entity',
            check='awesome_check',
        )

        with pytest.raises(AnsibleFailJson, match='Error'):
            event.main()

    def test_minimal_event_parameters(self, mocker):
        send_event_mock = mocker.patch.object(event, 'send_event')
        send_event_mock.return_value = True, {}
        get_entity_mock = mocker.patch.object(event, 'get_entity')
        get_entity_mock.return_value = dict(
            metadata=dict(
                name='awesome_entity',
                namespace='default'
            ),
            entity_class='proxy'
        )
        get_check_mock = mocker.patch.object(event, 'get_check')
        get_check_mock.return_value = dict(
            metadata=dict(
                name='awesome_check',
                namespace='default'
            )
        )

        set_module_args(
            entity='awesome_entity',
            check='awesome_check',
        )

        with pytest.raises(AnsibleExitJson):
            event.main()

        _client, path, payload, check_mode = send_event_mock.call_args[0]
        assert path == '/api/core/v2/namespaces/default/events/awesome_entity/awesome_check'
        assert payload == dict(
            metadata=dict(
                namespace='default'
            ),
            entity=dict(
                metadata=dict(
                    name='awesome_entity',
                    namespace='default'
                ),
                entity_class='proxy'
            ),
            check=dict(
                metadata=dict(
                    name='awesome_check',
                    namespace='default'
                )
            )
        )
        assert check_mode is False

    def test_all_event_parameters(self, mocker):
        entity_object = dict(
            metadata=dict(
                name='awesome_entity',
                namespace='default'
            ),
            entity_class='proxy'
        )
        check_object = dict(
            metadata=dict(
                name='awesome_check',
                namespace='default'
            ),
            command="check-cpu.sh -w 75 -c 90",
            handlers=["slack"],
            interval=60,
            publish=True,
            subscriptions=["linux"],
        )
        send_event_mock = mocker.patch.object(event, 'send_event')
        send_event_mock.return_value = True, {}
        get_entity_mock = mocker.patch.object(event, 'get_entity')
        get_entity_mock.return_value = entity_object
        get_check_mock = mocker.patch.object(event, 'get_check')
        get_check_mock.return_value = check_object

        set_module_args(
            namespace='my',
            timestamp=1234567,
            entity='awesome_entity',
            check='awesome_check',
            check_attributes=dict(
                duration=1.945,
                executed=1522100915,
                history=[
                    dict(
                        executed=1552505193,
                        status=1
                    ),
                    dict(
                        executed=1552505293,
                        status=0
                    ),
                    dict(
                        executed=1552505393,
                        status=0
                    ),
                    dict(
                        executed=1552505493,
                        status=0
                    )
                ],
                issued=1552506033,
                last_ok=1552506033,
                output='10',
                state='passing',
                status='ok',
                total_state_change=0
            ),
            metric_attributes=dict(
                handlers=['handler1', 'handler2'],
                points=[{
                    'name': 'sensu-go-sandbox.curl_timings.time_total',
                    'tags': [],
                    'timestamp': 1552506033,
                    'value': 0.005
                }, {
                    'name': 'sensu-go-sandbox.curl_timings.time_namelookup',
                    'tags': [],
                    'timestamp': 1552506033,
                    'value': 0.004
                }]
            )
        )

        with pytest.raises(AnsibleExitJson):
            event.main()

        _client, path, payload, check_mode = send_event_mock.call_args[0]
        assert path == '/api/core/v2/namespaces/my/events/awesome_entity/awesome_check'
        assert payload == dict(
            metadata=dict(
                namespace='my'
            ),
            timestamp=1234567,
            entity=dict(
                metadata=dict(
                    name='awesome_entity',
                    namespace='default'
                ),
                entity_class='proxy'
            ),
            check=dict(
                metadata=dict(
                    name='awesome_check',
                    namespace='default'
                ),
                command="check-cpu.sh -w 75 -c 90",
                handlers=["slack"],
                interval=60,
                publish=True,
                subscriptions=["linux"],
                duration=1.945,
                executed=1522100915,
                history=[
                    dict(
                        executed=1552505193,
                        status=1
                    ),
                    dict(
                        executed=1552505293,
                        status=0
                    ),
                    dict(
                        executed=1552505393,
                        status=0
                    ),
                    dict(
                        executed=1552505493,
                        status=0
                    )
                ],
                issued=1552506033,
                last_ok=1552506033,
                output='10',
                state='passing',
                status=0,
                total_state_change=0
            ),
            metrics=dict(
                handlers=['handler1', 'handler2'],
                points=[{
                    'name': 'sensu-go-sandbox.curl_timings.time_total',
                    'tags': [],
                    'timestamp': 1552506033,
                    'value': 0.005
                }, {
                    'name': 'sensu-go-sandbox.curl_timings.time_namelookup',
                    'tags': [],
                    'timestamp': 1552506033,
                    'value': 0.004
                }]
            )
        )
        assert check_mode is False

    def test_failure(self, mocker):
        get_entity_mock = mocker.patch.object(event, 'get_entity')
        get_entity_mock.side_effect = errors.Error('Bad error')
        set_module_args(
            entity='awesome_entity',
            check=dict(
                name='awesome_check'
            )
        )

        with pytest.raises(AnsibleFailJson):
            event.main()
