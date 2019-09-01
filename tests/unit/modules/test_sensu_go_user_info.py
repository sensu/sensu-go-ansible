from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.modules import sensu_go_user_info

from .common.utils import ModuleTestCase, generate_name
from .common.sensu_go_object_info import TestSensuGoObjectInfoBase


class TestSensuGoUserInfo(ModuleTestCase, TestSensuGoObjectInfoBase):
    module = sensu_go_user_info
    matrix = [
        dict(
            name='Fetch specific user',
            params={
                'name': 'test_user'
            },
            expect_result_key='users',
            expect_result=[{'name': 'test_user'}],
            expect_api_url='/api/core/v2/users/test_user',
            existing_object={'name': 'test_user'}
        ),
        dict(
            name='Fetch multiple users',
            params={},
            expect_result_key='users',
            expect_result=[{'name': 'test_user'}, {'name': 'test_user2'}],
            expect_api_url='/api/core/v2/users',
            existing_object=[{'name': 'test_user'}, {'name': 'test_user2'}]
        ),
        dict(
            name='Fetch unexisting user',
            params={
                'name': 'unexisting'
            },
            expect_result_key='users',
            expect_result=[{}],
            expect_api_url='/api/core/v2/users/unexisting',
            existing_object={}
        ),
        dict(
            name='Fetch zero users',
            params={},
            expect_result_key='users',
            expect_result=[],
            expect_api_url='/api/core/v2/users',
            existing_object=[]
        ),
        dict(
            name='(check) Test fetch users',
            params={
                'name': 'test_user'
            },
            check_mode=True,
            expect_result_key='users',
            expect_result=[{'name': 'test_user'}],
            expect_api_url='/api/core/v2/users/test_user',
            existing_object={'name': 'test_user'}
        ),
    ]

    @pytest.mark.parametrize('test_data', matrix, ids=generate_name)
    def test_module(self, test_data):
        self.run_test_case(test_data)
