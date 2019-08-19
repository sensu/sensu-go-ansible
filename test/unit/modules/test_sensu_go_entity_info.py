from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.modules import sensu_go_entity_info

from .common.utils import ModuleTestCase, generate_name
from .common.sensu_go_object_info import TestSensuGoObjectInfoBase


class TestSensuGoEntityInfo(ModuleTestCase, TestSensuGoObjectInfoBase):
    module = sensu_go_entity_info
    matrix = [
        dict(
            name='Fetch specific entity',
            params={
                'name': 'test_entity'
            },
            expect_result_key='entities',
            expect_result=[{'name': 'test_entity'}],
            expect_api_url='/api/core/v2/namespaces/default/entities/test_entity',
            existing_object={'name': 'test_entity'}
        ),
        dict(
            name='Fetch multiple entities',
            params={},
            expect_result_key='entities',
            expect_result=[{'name': 'test_entity'}, {'name': 'test_entity2'}],
            expect_api_url='/api/core/v2/namespaces/default/entities',
            existing_object=[{'name': 'test_entity'}, {'name': 'test_entity2'}]
        ),
        dict(
            name='Fetch unexisting entity',
            params={
                'name': 'unexisting'
            },
            expect_result_key='entities',
            expect_result=[{}],
            expect_api_url='/api/core/v2/namespaces/default/entities/unexisting',
            existing_object={}
        ),
        dict(
            name='Fetch zero entities',
            params={},
            expect_result_key='entities',
            expect_result=[],
            expect_api_url='/api/core/v2/namespaces/default/entities',
            existing_object=[]
        ),
        dict(
            name='(check) Test fetch entitiy',
            params={
                'name': 'test_entity'
            },
            check_mode=True,
            expect_result_key='entities',
            expect_result=[{'name': 'test_entity'}],
            expect_api_url='/api/core/v2/namespaces/default/entities/test_entity',
            existing_object={'name': 'test_entity'}
        ),
    ]

    @pytest.mark.parametrize('test_data', matrix, ids=generate_name)
    def test_module(self, test_data):
        self.run_test_case(test_data)
