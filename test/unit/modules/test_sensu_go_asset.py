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
                'name': 'test_asset',
                'download_url': 'http://example.com/asset.tar.gz',
                'sha512': 'sha512String',
            },
            is_http_error=True,
            expect_failed=True,
            expect_msg='authentication failed: unreachable'
        ),
        dict(
            name='Create Asset',
            params={
                'name': 'test_asset',
                'state': 'present',
                'download_url': 'http://example.com/asset.tar.gz',
                'sha512': 'sha512String'
            },
            expect_changed=True,
            expect_api_method='PUT',
            expect_api_url='/api/core/v2/namespaces/default/assets/test_asset',
            expect_api_headers={
                'Authorization': 'Bearer token',
                'Content-type': 'application/json'
            },
            expect_api_payload={
                'metadata': {
                    'name': 'test_asset',
                    'namespace': 'default'
                },
                'url': 'http://example.com/asset.tar.gz',
                'sha512': 'sha512String'
            }
        ),
        dict(
            name='Create Asset on different namespace',
            params={
                'name': 'test_asset',
                'namespace': 'testing_namespace',
                'state': 'present',
                'download_url': 'http://example.com/asset.tar.gz',
                'sha512': 'sha512String'
            },
            expect_changed=True,
            expect_api_method='PUT',
            expect_api_url='/api/core/v2/namespaces/testing_namespace/assets/test_asset',
            expect_api_headers={
                'Authorization': 'Bearer token',
                'Content-type': 'application/json'
            },
            expect_api_payload={
                'metadata': {
                    'name': 'test_asset',
                    'namespace': 'testing_namespace'
                },
                'url': 'http://example.com/asset.tar.gz',
                'sha512': 'sha512String'
            }
        ),
        dict(
            name='Test idempotency',
            params={
                'name': 'test_asset',
                'state': 'present',
                'download_url': 'http://example.com/asset.tar.gz',
                'sha512': 'sha512String',
                'filters': ["entity.system.os == 'linux'"],
                'headers': {'X-Test': 'Test'}
            },
            expect_changed=False,
            existing_object={
                'metadata': {
                    'name': 'test_asset',
                    'namespace': 'default'
                },
                'url': 'http://example.com/asset.tar.gz',
                'sha512': 'sha512String',
                'filters': ["entity.system.os == 'linux'"],
                'headers': {'X-Test': 'Test'}
            }
        ),
        dict(
            name='Update existing asset',
            params={
                'name': 'test_asset',
                'download_url': 'http://example.com/new-asset.tar.gz',
                'sha512': 'new-sha512String',
                'filters': ["new.filter == 'new'"],
                'headers': {'X-Test': 'new-header'}
            },
            expect_changed=True,
            expect_api_method='PUT',
            expect_api_url='/api/core/v2/namespaces/default/assets/test_asset',
            expect_api_headers={
                'Authorization': 'Bearer token',
                'Content-type': 'application/json'
            },
            expect_api_payload={
                'metadata': {
                    'name': 'test_asset',
                    'namespace': 'default'
                },
                'url': 'http://example.com/new-asset.tar.gz',
                'sha512': 'new-sha512String',
                'filters': ["new.filter == 'new'"],
                'headers': {'X-Test': 'new-header'}
            },
            existing_object={
                'metadata': {
                    'name': 'test_asset',
                    'namespace': 'default'
                },
                'url': 'http://example.com/asset.tar.gz',
                'sha512': 'sha512String',
                'filters': ["entity.system.os == 'linux'"],
                'headers': {'X-Test': 'Test'}
            }
        ),
        dict(
            name='(check) Create Asset',
            params={
                'name': 'test_asset',
                'state': 'present',
                'download_url': 'http://example.com/asset.tar.gz',
                'sha512': 'sha512String',
                'filters': ["entity.system.os == 'linux'"],
                'headers': {'X-Test': 'Test'}
            },
            check_mode=True,
            expect_changed=True,
        ),
        dict(
            name='(check) Update Asset',
            params={
                'name': 'test_asset',
                'download_url': 'http://example.com/new-asset.tar.gz',
                'sha512': 'new-sha512String',
                'filters': ["new.filter == 'new'"],
                'headers': {'X-Test': 'new-header'}
            },
            check_mode=True,
            expect_changed=True,
            existing_object={
                'metadata': {
                    'name': 'test_asset',
                    'namespace': 'default'
                },
                'url': 'http://example.com/asset.tar.gz',
                'sha512': 'sha512String',
                'filters': ["entity.system.os == 'linux'"],
                'headers': {'X-Test': 'Test'}
            }
        ),
        dict(
            name='(check) Update Asset idempotency',
            params={
                'name': 'test_asset',
                'state': 'present',
                'download_url': 'http://example.com/asset.tar.gz',
                'sha512': 'sha512String',
                'filters': ["entity.system.os == 'linux'"],
                'headers': {'X-Test': 'Test'}
            },
            check_mode=True,
            expect_changed=False,
            existing_object={
                'metadata': {
                    'name': 'test_asset',
                    'namespace': 'default'
                },
                'url': 'http://example.com/asset.tar.gz',
                'sha512': 'sha512String',
                'filters': ["entity.system.os == 'linux'"],
                'headers': {'X-Test': 'Test'}
            }
        ),
    ], ids=generate_name)
    def test_asset_module(self, test_data):
        self.run_test_case(test_data)
