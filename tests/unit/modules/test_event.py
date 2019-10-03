from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, utils,
)
from ansible_collections.sensu.sensu_go.plugins.modules import event

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)


class TestEvent(ModuleTestCase):
    def test_minimal_event_parameters(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.return_value = True, {}
        set_module_args(
            entity=dict(
                metadata=dict(
                    name='awesome_entity'
                ),
                entity_class='proxy'
            ),
            check=dict(
                metadata=dict(
                    name='awesome_check'
                )
            )
        )

        with pytest.raises(AnsibleExitJson):
            event.main()

        state, _client, path, payload, check_mode = sync_mock.call_args[0]
        assert state == 'present'
        assert path == '/events/awesome_entity/awesome_check'
        assert payload == dict(
            metadata=dict(
                namespace='default'
            ),
            entity=dict(
                metadata=dict(
                    name='awesome_entity'
                ),
                entity_class='proxy'
            ),
            check=dict(
                metadata=dict(
                    name='awesome_check'
                )
            )
        )
        assert check_mode is False

    def test_all_event_parameters(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.return_value = True, {}
        set_module_args(
            timestamp=1234567,
            state='absent',
            entity=dict(
                metadata=dict(
                    name='awesome_entity'
                ),
                entity_class='proxy'
            ),
            check=dict(
                metadata=dict(
                    name='awesome_check'
                )
            ),
            check_merge=dict(
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
                output='sensu-go-sandbox.curl_timings.time_total 0.005',
                state='passing',
                status='ok',
                total_state_change=0
            )
        )

        with pytest.raises(AnsibleExitJson):
            event.main()

        state, _client, path, payload, check_mode = sync_mock.call_args[0]
        assert state == 'absent'
        assert path == '/events/awesome_entity/awesome_check'
        assert payload == dict(
            metadata=dict(
                namespace='default'
            ),
            timestamp=1234567,
            entity=dict(
                metadata=dict(
                    name='awesome_entity'
                ),
                entity_class='proxy'
            ),
            check=dict(
                metadata=dict(
                    name='awesome_check'
                ),
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
                output='sensu-go-sandbox.curl_timings.time_total 0.005',
                state='passing',
                status=0,
                total_state_change=0
            )
        )
        assert check_mode is False

    def test_failure(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.side_effect = errors.Error('Bad error')
        set_module_args(
            entity=dict(
                metadata=dict(
                    name='awesome_entity'
                ),
                entity_class='proxy'
            ),
            check=dict(
                metadata=dict(
                    name='awesome_check'
                )
            )
        )

        with pytest.raises(AnsibleFailJson):
            event.main()
