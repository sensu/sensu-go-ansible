from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.modules import sensu_go_event_info

from .common.utils import ModuleTestCase, generate_name
from .common.sensu_go_object_info import TestSensuGoObjectInfoBase


class TestSensuGoEventInfo(ModuleTestCase, TestSensuGoObjectInfoBase):
    module = sensu_go_event_info
    matrix = [
        dict(
            name='Fetch all events',
            params={},
            expect_result_key='events',
            expect_result=[{'name': 'test_event'}],
            expect_api_url='/api/core/v2/namespaces/default/events',
            existing_object=[{'name': 'test_event'}]
        ),
        dict(
            name='Fetch all events by entity',
            params={
                'entity': 'test_entity'
            },
            expect_result_key='events',
            expect_result=[{'name': 'test_event'}],
            expect_api_url='/api/core/v2/namespaces/default/events/test_entity',
            existing_object=[{'name': 'test_event'}]
        ),
        dict(
            name='Fetch all events by entity and check',
            params={
                'entity': 'test_entity',
                'check': 'test_check',
            },
            expect_result_key='events',
            expect_result=[{'name': 'test_event'}],
            expect_api_url='/api/core/v2/namespaces/default/events/test_entity/test_check',
            existing_object={'name': 'test_event'}
        ),
        dict(
            name='Fetch zero events',
            params={},
            expect_result_key='events',
            expect_result=[],
            expect_api_url='/api/core/v2/namespaces/default/events',
            existing_object=[]
        ),
        dict(
            name='(check) Test fetch event',
            params={},
            check_mode=True,
            expect_result_key='events',
            expect_result=[{'name': 'test_event'}],
            expect_api_url='/api/core/v2/namespaces/default/events',
            existing_object=[{'name': 'test_event'}]
        ),
    ]

    @pytest.mark.parametrize('test_data', matrix, ids=generate_name)
    def test_module(self, test_data):
        self.run_test_case(test_data)
