from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.modules import sensu_go_silence_info

from .common.utils import ModuleTestCase, generate_name
from .common.sensu_go_object_info import TestSensuGoObjectInfoBase


class TestSensuGoSilenceInfo(ModuleTestCase, TestSensuGoObjectInfoBase):
    module = sensu_go_silence_info
    matrix = [
        dict(
            name='Fetch specific silenced',
            params={
                'name': 'test_silenced'
            },
            expect_result_key='silenced',
            expect_result=[{'name': 'test_silenced'}],
            expect_api_url='/api/core/v2/namespaces/default/silenced/test_silenced',
            existing_object={'name': 'test_silenced'}
        ),
        dict(
            name='Fetch all silenced',
            params={},
            expect_result_key='silenced',
            expect_result=[{'name': 'test_silenced'}],
            expect_api_url='/api/core/v2/namespaces/default/silenced',
            existing_object=[{'name': 'test_silenced'}]
        ),
        dict(
            name='Fetch silenced per subscription',
            params={
                'subscription': 'test_subscription'
            },
            expect_result_key='silenced',
            expect_result=[{'name': 'test_silenced'}],
            expect_api_url='/api/core/v2/namespaces/default/silenced/subscriptions/test_subscription',
            existing_object=[{'name': 'test_silenced'}]
        ),
        dict(
            name='Fetch silenced per check',
            params={
                'check': 'test_check'
            },
            expect_result_key='silenced',
            expect_result=[{'name': 'test_silenced'}],
            expect_api_url='/api/core/v2/namespaces/default/silenced/checks/test_check',
            existing_object=[{'name': 'test_silenced'}]
        ),
        dict(
            name='(check) Test fetch all silenced',
            params={},
            check_mode=True,
            expect_result_key='silenced',
            expect_result=[{'name': 'test_silenced'}],
            expect_api_url='/api/core/v2/namespaces/default/silenced',
            existing_object=[{'name': 'test_silenced'}]
        ),
    ]

    @pytest.mark.parametrize('test_data', matrix, ids=generate_name)
    def test_module(self, test_data):
        self.run_test_case(test_data)
