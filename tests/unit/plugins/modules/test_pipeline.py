from __future__ import absolute_import, division, print_function
__metaclass__ = type

import sys

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, utils,
)
from ansible_collections.sensu.sensu_go.plugins.modules import pipeline

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestDoDiffer:
    @pytest.mark.parametrize("current,desired", [
        (  # No diff in params, no secrets
            dict(name="demo"),
            dict(name="demo"),
        ),
    ])
    def test_no_difference(self, current, desired):
        assert pipeline.do_differ(current, desired) is False

    @pytest.mark.parametrize("current,desired", [
        (  # Diff in params, no diff in secrets
            dict(name="demo", secrets=[dict(name="a", secret="1")]),
            dict(name="prod", secrets=[dict(name="a", secret="1")]),
        ),
        (  # No diff in params, missing and set secrets
            dict(name="demo", secrets=[dict(name="a", secret="1")]),
            dict(name="demo", secrets=[dict(name="b", secret="2")]),
        ),
        (  # Diff in params, missing and set secrets
            dict(name="demo", secrets=[dict(name="a", secret="1")]),
            dict(name="prod", secrets=[dict(name="b", secret="2")]),
        ),
    ])
    def test_difference(self, current, desired):
        assert pipeline.do_differ(current, desired) is True


class TestHandle(ModuleTestCase):
    def test_handle_api_version_and_types(self, mocker):
        module = mocker.patch('ansible.module_utils.basic.AnsibleModule')
        module.params = dict(workflows=[dict(handler=dict(name="test_handler", type="handler"))])
        payload = dict(workflows=[dict(handler=dict(name="test_handler", type="handler"))])
        pipeline.handle_api_version_and_types(module, payload)
        expected = dict(
            workflows=[dict(
                handler=dict(name="test_handler", type="Handler", api_version="core/v2")
            )]
        )
        assert module.params != payload
        assert payload == expected

    @pytest.mark.parametrize("payload_handler, expected", [
        (
            dict(name="test_handler", type="handler"),
            dict(name="test_handler", type="Handler", api_version="core/v2"),
        ),
        (
            dict(name="test_handler", type="tcp_stream_handler"),
            dict(name="test_handler", type="TCPStreamHandler", api_version="pipeline/v1"),
        ),
        (
            dict(name="test_handler", type="sumo_logic_metrics_handler"),
            dict(name="test_handler", type="SumoLogicMetricsHandler", api_version="pipeline/v1"),
        ),
    ])
    def test_handle_handler_api_and_type(self, payload_handler, expected):
        pipeline.handle_handler_api_and_type(payload_handler)
        assert payload_handler == expected

    @pytest.mark.parametrize("payload_mutator, expected", [
        (
            dict(name="test_mutator", type="mutator"),
            dict(name="test_mutator", type="Mutator", api_version="core/v2"),
        ),
    ])
    def test_handle_mutator_api_and_type(self, payload_mutator, expected):
        pipeline.handle_mutator_api_and_type(payload_mutator)
        assert payload_mutator == expected

    @pytest.mark.parametrize("workflow, payload_filters, expected", [
        (
            dict(filters=[dict(name="test_filter", type="event_filter")]),
            [dict(name="test_filter", type="event_filter")],
            [dict(name="test_filter", type="EventFilter", api_version="core/v2")],
        ),
        (
            dict(filters=[dict(name="test_filter", type="event_filter"),
                          dict(name="test_filter_2", type="event_filter")]),
            [dict(name="test_filter", type="event_filter"), dict(name="test_filter_2", type="event_filter")],
            [dict(name="test_filter", type="EventFilter", api_version="core/v2"),
                dict(name="test_filter_2", type="EventFilter", api_version="core/v2")],
        ),
    ])
    def test_handle_filter_api_and_type(self, workflow, payload_filters, expected):
        pipeline.handle_filter_api_and_type(payload_filters, workflow)
        assert payload_filters == expected


class TestPipeline(ModuleTestCase):
    def test_minimal_pipeline_parameters(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.return_value = True, {}
        set_module_args(
            name='test_pipeline',
            workflows=[dict(name='test_wf', handler=dict(name='test_handler', type='handler'))]
        )

        with pytest.raises(AnsibleExitJson):
            pipeline.main()

        state, _client, path, payload, check_mode, _d = sync_mock.call_args[0]
        assert state == 'present'
        assert path == '/api/core/v2/namespaces/default/pipelines/test_pipeline'
        assert payload == dict(
            workflows=[dict(
                name='test_wf', handler=dict(
                    name='test_handler', type='Handler', api_version='core/v2'))],
            metadata=dict(
                name='test_pipeline',
                namespace='default',
            ),
        )
        assert check_mode is False

    def test_all_pipeline_parameters(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.return_value = True, {}
        set_module_args(
            name='test_pipeline',
            namespace='my',
            state='absent',
            workflows=[dict(name='test_wf', handler=dict(name='test_handler', type='handler'),
                            filters=[dict(name='test_filter', type='event_filter')],
                            mutator=dict(name='test_mutator', type='mutator')
                            )
                       ],
            labels={'region': 'us-west-1'}
        )

        with pytest.raises(AnsibleExitJson):
            pipeline.main()

        state, _client, path, payload, check_mode, _d = sync_mock.call_args[0]
        assert state == 'absent'
        assert path == '/api/core/v2/namespaces/my/pipelines/test_pipeline'
        assert payload == dict(
            metadata=dict(
                name='test_pipeline',
                namespace='my',
                labels={'region': 'us-west-1'},
            ),
            workflows=[dict(name='test_wf', handler=dict(name='test_handler', type='handler'),
                            filters=[dict(name='test_filter', type='event_filter')],
                            mutator=dict(name='test_mutator', type='mutator')
                            )]
        )
        assert check_mode is False

    def test_failure(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.side_effect = errors.Error('Bad error')
        set_module_args(
            name='test_pipeline',
        )

        with pytest.raises(AnsibleFailJson):
            pipeline.main()
