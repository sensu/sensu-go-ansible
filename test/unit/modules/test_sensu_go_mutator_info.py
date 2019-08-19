from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.modules import sensu_go_mutator_info

from .common.utils import ModuleTestCase, generate_name
from .common.sensu_go_object_info import TestSensuGoObjectInfoBase


class TestSensuGoMutatorInfo(ModuleTestCase, TestSensuGoObjectInfoBase):
    module = sensu_go_mutator_info
    matrix = [
        dict(
            name='Fetch specific mutator',
            params={
                'name': 'test_mutator'
            },
            expect_result_key='mutators',
            expect_result=[{'name': 'test_mutator'}],
            expect_api_url='/api/core/v2/namespaces/default/mutators/test_mutator',
            existing_object={'name': 'test_mutator'}
        ),
        dict(
            name='Fetch multiple mutators',
            params={},
            expect_result_key='mutators',
            expect_result=[{'name': 'test_mutator'}, {'name': 'test_mutator2'}],
            expect_api_url='/api/core/v2/namespaces/default/mutators',
            existing_object=[{'name': 'test_mutator'}, {'name': 'test_mutator2'}]
        ),
        dict(
            name='Fetch unexisting mutator',
            params={
                'name': 'unexisting'
            },
            expect_result_key='mutators',
            expect_result=[{}],
            expect_api_url='/api/core/v2/namespaces/default/mutators/unexisting',
            existing_object={}
        ),
        dict(
            name='Fetch zero mutators',
            params={},
            expect_result_key='mutators',
            expect_result=[],
            expect_api_url='/api/core/v2/namespaces/default/mutators',
            existing_object=[]
        ),
        dict(
            name='(check) Test fetch mutator',
            params={
                'name': 'test_mutator'
            },
            check_mode=True,
            expect_result_key='mutators',
            expect_result=[{'name': 'test_mutator'}],
            expect_api_url='/api/core/v2/namespaces/default/mutators/test_mutator',
            existing_object={'name': 'test_mutator'}
        ),
    ]

    @pytest.mark.parametrize('test_data', matrix, ids=generate_name)
    def test_module(self, test_data):
        self.run_test_case(test_data)
