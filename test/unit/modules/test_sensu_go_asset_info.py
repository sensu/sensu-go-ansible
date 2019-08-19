from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.modules import sensu_go_asset_info

from .common.utils import ModuleTestCase, generate_name
from .common.sensu_go_object_info import TestSensuGoObjectInfoBase


class TestSensuGoAssetInfo(ModuleTestCase, TestSensuGoObjectInfoBase):
    module = sensu_go_asset_info
    matrix = [
        dict(
            name='Fetch specific asset',
            params={
                'name': 'test_asset'
            },
            expect_result_key='assets',
            expect_result=[{'name': 'test_asset'}],
            expect_api_url='/api/core/v2/namespaces/default/assets/test_asset',
            existing_object={'name': 'test_asset'}
        ),
        dict(
            name='Fetch multiple assets',
            params={},
            expect_result_key='assets',
            expect_result=[{'name': 'test_asset'}, {'name': 'asset2'}],
            expect_api_url='/api/core/v2/namespaces/default/assets',
            existing_object=[{'name': 'test_asset'}, {'name': 'asset2'}]
        ),
        dict(
            name='Fetch unexisting asset',
            params={
                'name': 'test_asset'
            },
            expect_result_key='assets',
            expect_result=[{}],
            expect_api_url='/api/core/v2/namespaces/default/assets/test_asset',
            existing_object={}
        ),
        dict(
            name='Fetch unexisting assets',
            params={},
            expect_result_key='assets',
            expect_result=[],
            expect_api_url='/api/core/v2/namespaces/default/assets',
            existing_object=[]
        ),
        dict(
            name='(check) Test fetch assets',
            params={
                'name': 'test_asset'
            },
            check_mode=True,
            expect_result_key='assets',
            expect_result=[{'name': 'test_asset'}],
            expect_api_url='/api/core/v2/namespaces/default/assets/test_asset',
            existing_object={'name': 'test_asset'}
        ),
    ]

    @pytest.mark.parametrize('test_data', matrix, ids=generate_name)
    def test_module(self, test_data):
        self.run_test_case(test_data)
