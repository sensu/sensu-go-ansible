from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.modules import sensu_go_rolebinding_info

from .common.utils import ModuleTestCase, generate_name
from .common.sensu_go_object_info import TestSensuGoObjectInfoBase


class TestSensuGoRolebindingInfo(ModuleTestCase, TestSensuGoObjectInfoBase):
    module = sensu_go_rolebinding_info
    matrix = [
        dict(
            name='Fetch specific rolebinding (namespaced)',
            params={
                'name': 'test_binding'
            },
            expect_result_key='rolebindings',
            expect_result=[{'name': 'test_binding'}],
            expect_api_url='/api/core/v2/namespaces/default/rolebindings/test_binding',
            existing_object={'name': 'test_binding'}
        ),
        dict(
            name='Fetch specific rolebinding (cluster-wide)',
            params={
                'name': 'test_binding',
                'cluster': 'yes'
            },
            expect_result_key='rolebindings',
            expect_result=[{'name': 'test_binding'}],
            expect_api_url='/api/core/v2/clusterrolebindings/test_binding',
            existing_object={'name': 'test_binding'}
        ),
        dict(
            name='Fetch multiple rolebinding (namespaced)',
            params={},
            expect_result_key='rolebindings',
            expect_result=[{'name': 'test_binding'}, {'name': 'test_binding2'}],
            expect_api_url='/api/core/v2/namespaces/default/rolebindings',
            existing_object=[{'name': 'test_binding'}, {'name': 'test_binding2'}]
        ),
        dict(
            name='Fetch multiple rolebinding (cluster-wide)',
            params={
                'cluster': 'yes'
            },
            expect_result_key='rolebindings',
            expect_result=[{'name': 'test_binding'}, {'name': 'test_binding2'}],
            expect_api_url='/api/core/v2/clusterrolebindings',
            existing_object=[{'name': 'test_binding'}, {'name': 'test_binding2'}]
        ),
        dict(
            name='Fetch unexisting rolebinding (namespaced)',
            params={
                'name': 'unexisting'
            },
            expect_result_key='rolebindings',
            expect_result=[{}],
            expect_api_url='/api/core/v2/namespaces/default/rolebindings/unexisting',
            existing_object={}
        ),
        dict(
            name='Fetch unexisting rolebinding (cluster-wide)',
            params={
                'name': 'unexisting',
                'cluster': 'yes'
            },
            expect_result_key='rolebindings',
            expect_result=[{}],
            expect_api_url='/api/core/v2/clusterrolebindings/unexisting',
            existing_object={}
        ),
        dict(
            name='Fetch zero rolebindings (namespaced)',
            params={},
            expect_result_key='rolebindings',
            expect_result=[],
            expect_api_url='/api/core/v2/namespaces/default/rolebindings',
            existing_object=[]
        ),
        dict(
            name='Fetch zero rolebindings (cluster-wide)',
            params={
                'cluster': 'yes'
            },
            expect_result_key='rolebindings',
            expect_result=[],
            expect_api_url='/api/core/v2/clusterrolebindings',
            existing_object=[]
        ),
        dict(
            name='(check) Test fetch rolebindig (namespaced)',
            params={
                'name': 'test_binding'
            },
            check_mode=True,
            expect_result_key='rolebindings',
            expect_result=[{'name': 'test_binding'}],
            expect_api_url='/api/core/v2/namespaces/default/rolebindings/test_binding',
            existing_object={'name': 'test_binding'}
        ),
        dict(
            name='(check) Test fetch rolebindig (cluster-wide)',
            params={
                'name': 'test_binding',
                'cluster': 'yes'
            },
            check_mode=True,
            expect_result_key='rolebindings',
            expect_result=[{'name': 'test_binding'}],
            expect_api_url='/api/core/v2/clusterrolebindings/test_binding',
            existing_object={'name': 'test_binding'}
        ),
    ]

    @pytest.mark.parametrize('test_data', matrix, ids=generate_name)
    def test_module(self, test_data):
        self.run_test_case(test_data)
