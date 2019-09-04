from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.modules import sensu_go_check_info

from .common.utils import ModuleTestCase, generate_name
from .common.sensu_go_object_info import TestSensuGoObjectInfoBase


class TestSensuGoCheckInfo(ModuleTestCase, TestSensuGoObjectInfoBase):
    module = sensu_go_check_info
    matrix = [
        dict(
            name='Fetch specific check',
            params={
                'name': 'test_check'
            },
            expect_result_key='checks',
            expect_result=[{'name': 'test_check'}],
            expect_api_url='/api/core/v2/namespaces/default/checks/test_check',
            existing_object={'name': 'test_check'}
        ),
        dict(
            name='Fetch multiple checks',
            params={},
            expect_result_key='checks',
            expect_result=[{'name': 'test_check'}, {'name': 'test_check2'}],
            expect_api_url='/api/core/v2/namespaces/default/checks',
            existing_object=[{'name': 'test_check'}, {'name': 'test_check2'}]
        ),
        dict(
            name='Fetch unexisting check',
            params={
                'name': 'unexisting'
            },
            expect_result_key='checks',
            expect_result=[{}],
            expect_api_url='/api/core/v2/namespaces/default/checks/unexisting',
            existing_object={}
        ),
        dict(
            name='Fetch zero checks',
            params={},
            expect_result_key='checks',
            expect_result=[],
            expect_api_url='/api/core/v2/namespaces/default/checks',
            existing_object=[]
        ),
        dict(
            name='(check) Test fetch check',
            params={
                'name': 'test_check'
            },
            check_mode=True,
            expect_result_key='checks',
            expect_result=[{'name': 'test_check'}],
            expect_api_url='/api/core/v2/namespaces/default/checks/test_check',
            existing_object={'name': 'test_check'}
        ),
    ]

    @pytest.mark.parametrize('test_data', matrix, ids=generate_name)
    def test_module(self, test_data):
        self.run_test_case(test_data)
