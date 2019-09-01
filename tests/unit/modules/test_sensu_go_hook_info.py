from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.modules import sensu_go_hook_info

from .common.utils import ModuleTestCase, generate_name
from .common.sensu_go_object_info import TestSensuGoObjectInfoBase


class TestSensuGoHookInfo(ModuleTestCase, TestSensuGoObjectInfoBase):
    module = sensu_go_hook_info
    matrix = [
        dict(
            name='Fetch specific hook',
            params={
                'name': 'test_hook'
            },
            expect_result_key='hooks',
            expect_result=[{'name': 'test_hook'}],
            expect_api_url='/api/core/v2/namespaces/default/hooks/test_hook',
            existing_object={'name': 'test_hook'}
        ),
        dict(
            name='Fetch multiple hooks',
            params={},
            expect_result_key='hooks',
            expect_result=[{'name': 'test_hook'}, {'name': 'test_hook2'}],
            expect_api_url='/api/core/v2/namespaces/default/hooks',
            existing_object=[{'name': 'test_hook'}, {'name': 'test_hook2'}]
        ),
        dict(
            name='Fetch unexisting hook',
            params={
                'name': 'unexisting'
            },
            expect_result_key='hooks',
            expect_result=[{}],
            expect_api_url='/api/core/v2/namespaces/default/hooks/unexisting',
            existing_object={}
        ),
        dict(
            name='Fetch zero hooks',
            params={},
            expect_result_key='hooks',
            expect_result=[],
            expect_api_url='/api/core/v2/namespaces/default/hooks',
            existing_object=[]
        ),
        dict(
            name='(check) Test fetch hook',
            params={
                'name': 'test_hook'
            },
            check_mode=True,
            expect_result_key='hooks',
            expect_result=[{'name': 'test_hook'}],
            expect_api_url='/api/core/v2/namespaces/default/hooks/test_hook',
            existing_object={'name': 'test_hook'}
        ),
    ]

    @pytest.mark.parametrize('test_data', matrix, ids=generate_name)
    def test_module(self, test_data):
        self.run_test_case(test_data)
