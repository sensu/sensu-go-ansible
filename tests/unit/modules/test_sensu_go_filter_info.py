from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.modules import sensu_go_filter_info

from .common.utils import ModuleTestCase, generate_name
from .common.sensu_go_object_info import TestSensuGoObjectInfoBase


class TestSensuGoFilterInfo(ModuleTestCase, TestSensuGoObjectInfoBase):
    module = sensu_go_filter_info
    matrix = [
        dict(
            name='Fetch specific filter',
            params={
                'name': 'test_filter'
            },
            expect_result_key='filters',
            expect_result=[{'name': 'test_filter'}],
            expect_api_url='/api/core/v2/namespaces/default/filters/test_filter',
            existing_object={'name': 'test_filter'}
        ),
        dict(
            name='Fetch multiple filters',
            params={},
            expect_result_key='filters',
            expect_result=[{'name': 'test_filter'}, {'name': 'test_filter2'}],
            expect_api_url='/api/core/v2/namespaces/default/filters',
            existing_object=[{'name': 'test_filter'}, {'name': 'test_filter2'}]
        ),
        dict(
            name='Fetch unexisting filter',
            params={
                'name': 'unexisting'
            },
            expect_result_key='filters',
            expect_result=[{}],
            expect_api_url='/api/core/v2/namespaces/default/filters/unexisting',
            existing_object={}
        ),
        dict(
            name='Fetch zero filters',
            params={},
            expect_result_key='filters',
            expect_result=[],
            expect_api_url='/api/core/v2/namespaces/default/filters',
            existing_object=[]
        ),
        dict(
            name='(check) Test fetch filter',
            params={
                'name': 'test_filter'
            },
            check_mode=True,
            expect_result_key='filters',
            expect_result=[{'name': 'test_filter'}],
            expect_api_url='/api/core/v2/namespaces/default/filters/test_filter',
            existing_object={'name': 'test_filter'}
        ),
    ]

    @pytest.mark.parametrize('test_data', matrix, ids=generate_name)
    def test_module(self, test_data):
        self.run_test_case(test_data)
