from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.modules import sensu_go_cluster_info

from .common.utils import ModuleTestCase, generate_name
from .common.sensu_go_object_info import TestSensuGoObjectInfoBase


class TestSensuGoClusterInfo(ModuleTestCase, TestSensuGoObjectInfoBase):
    module = sensu_go_cluster_info
    matrix = [
        dict(
            name='Fetch cluster members',
            params={},
            expect_result_key='cluster',
            expect_result=[{'name': 'member'}, {'name': 'member2'}],
            expect_api_url='/api/core/v2/cluster/members',
            existing_object=[{'name': 'member'}, {'name': 'member2'}]
        ),
        dict(
            name='Fetch zero cluster members',
            params={},
            expect_result_key='cluster',
            expect_result=[],
            expect_api_url='/api/core/v2/cluster/members',
            existing_object=[]
        ),
        dict(
            name='(check) Test fetch cluster members',
            params={},
            check_mode=True,
            expect_result_key='cluster',
            expect_result=[{'name': 'member'}],
            expect_api_url='/api/core/v2/cluster/members',
            existing_object=[{'name': 'member'}]
        ),
    ]

    @pytest.mark.parametrize('test_data', matrix, ids=generate_name)
    def test_module(self, test_data):
        self.run_test_case(test_data)
