import pytest

from ansible_collections.sensu.sensu_go.plugins.modules import sensu_go_asset
from ansible_collections.sensu.sensu_go.test.unit.modules.common.utils import ModuleTestCase, generate_name
from ansible_collections.sensu.sensu_go.test.unit.modules.common.sensu_go_object import TestSensuGoObjectBase


class TestSensuAssetModule(ModuleTestCase, TestSensuGoObjectBase):
    module = sensu_go_asset

    @pytest.mark.parametrize('test_data', [
        dict(
            name='Test unreachable URL',
            params={
                'url': 'http://test:8080',
                'name': 'test_asset',
                'download_url': 'http://example.com/asset.tar.gz',
                'sha512': 'sha512String',
            },
            is_http_error=True,
            expect_failed=True,
            expect_msg='authentication failed: unreachable'
        ),
        dict(
            name='Test create Asset',
            params={
                'url': 'http://test:8080',
                'name': 'test_asset',
                'state': 'present',
                'download_url': 'http://example.com/asset.tar.gz',
                'sha512': 'sha512String',
                'filters': ["entity.system.os == 'linux'"],
                'headers': {'X-Test': 'Test'}
            },
            expect_changed=True,
            expect_api_method='PUT',
            expect_api_url='http://test:8080/api/core/v2/namespaces/default/assets/test_asset',
            expect_api_headers={
                'Authorization': 'Bearer token',
                'Content-type': 'application/json'
            }
        )
    ], ids=generate_name)
    def test_asset_module(self, test_data):
        self.run_test_case(test_data)

    def _prepare_expected_data(self, params):
        ret_val = super(TestSensuAssetModule, self)._prepare_expected_data(params)
        ret_val['url'] = params.pop('download_url')
        return ret_val
