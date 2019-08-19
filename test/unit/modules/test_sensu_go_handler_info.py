from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.modules import sensu_go_handler_info

from .common.utils import ModuleTestCase, generate_name
from .common.sensu_go_object_info import TestSensuGoObjectInfoBase


class TestSensuGoHandlerInfo(ModuleTestCase, TestSensuGoObjectInfoBase):
    module = sensu_go_handler_info
    matrix = [
        dict(
            name='Fetch specific handler',
            params={
                'name': 'test_handler'
            },
            expect_result_key='handlers',
            expect_result=[{'name': 'test_handler'}],
            expect_api_url='/api/core/v2/namespaces/default/handlers/test_handler',
            existing_object={'name': 'test_handler'}
        ),
        dict(
            name='Fetch multiple handlers',
            params={},
            expect_result_key='handlers',
            expect_result=[{'name': 'test_handler'}, {'name': 'test_handler2'}],
            expect_api_url='/api/core/v2/namespaces/default/handlers',
            existing_object=[{'name': 'test_handler'}, {'name': 'test_handler2'}]
        ),
        dict(
            name='Fetch unexisting handler',
            params={
                'name': 'unexisting'
            },
            expect_result_key='handlers',
            expect_result=[{}],
            expect_api_url='/api/core/v2/namespaces/default/handlers/unexisting',
            existing_object={}
        ),
        dict(
            name='Fetch zero handlers',
            params={},
            expect_result_key='handlers',
            expect_result=[],
            expect_api_url='/api/core/v2/namespaces/default/handlers',
            existing_object=[]
        ),
        dict(
            name='(check) Test fetch handler',
            params={
                'name': 'test_handler'
            },
            check_mode=True,
            expect_result_key='handlers',
            expect_result=[{'name': 'test_handler'}],
            expect_api_url='/api/core/v2/namespaces/default/handlers/test_handler',
            existing_object={'name': 'test_handler'}
        ),
    ]

    @pytest.mark.parametrize('test_data', matrix, ids=generate_name)
    def test_module(self, test_data):
        self.run_test_case(test_data)
