from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.modules import sensu_go_namespace_info

from .common.utils import ModuleTestCase, generate_name
from .common.sensu_go_object_info import TestSensuGoObjectInfoBase


class TestSensuGoNamespaceInfo(ModuleTestCase, TestSensuGoObjectInfoBase):
    module = sensu_go_namespace_info
    matrix = [
        dict(
            name='Fetch multiple namespaces',
            params={},
            expect_result_key='namespaces',
            expect_result=['test_namespace', 'test_namespace2'],
            expect_api_url='/api/core/v2/namespaces',
            existing_object=[{'name': 'test_namespace'}, {'name': 'test_namespace2'}]
        ),
        dict(
            name='Fetch zero namespaces',
            params={},
            expect_result_key='namespaces',
            expect_result=[],
            expect_api_url='/api/core/v2/namespaces',
            existing_object=[]
        ),
        dict(
            name='(check) Test fetch namespaces',
            params={},
            check_mode=True,
            expect_result_key='namespaces',
            expect_result=['test_namespace'],
            expect_api_url='/api/core/v2/namespaces',
            existing_object=[{'name': 'test_namespace'}]
        ),
    ]

    @pytest.mark.parametrize('test_data', matrix, ids=generate_name)
    def test_module(self, test_data):
        self.run_test_case(test_data)
