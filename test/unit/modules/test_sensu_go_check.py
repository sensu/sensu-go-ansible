from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.modules import sensu_go_check

from .common.utils import ModuleTestCase, generate_name
from .common.sensu_go_object import TestSensuGoObjectBase


class TestSensuGoCheck(ModuleTestCase, TestSensuGoObjectBase):
    module = sensu_go_check
    matrix = [
        dict(
            name='Test unreachable URL',
            params={
                'name': 'test_check',
                'command': 'echo "test"',
                'subscriptions': ['switches'],
                'interval': 60
            },
            is_http_error=True,
            expect_failed=True,
            expect_msg='authentication failed: unreachable'
        ),
        dict(
            name='Create Check',
            params={
                'name': 'test_check',
                'command': 'echo "test"',
                'subscriptions': ['switches'],
                'handlers': ['email'],
                'interval': 60,
                'publish': True,
                'timeout': 30,
                'ttl': 100,
                'stdin': False,
                'env_vars': {'RUBY_VERSION': '2.5.0'},
                'low_flap_threshold': 20,
                'high_flap_threshold': 60,
                'runtime_assets': ['ruby-2.5.0'],
                'check_hooks': {},
                'proxy_entity_name': 'switch-dc-01',
                'proxy_entity_attributes': ['entity.entity_class == "proxy"'],
                'proxy_splay': True,
                'proxy_splay_coverage': 90,
                'output_metric_format': 'nagios_perfdata',
                'output_metric_handlers': ['influx-db'],
                'round_robin': True
            },
            expect_changed=True,
            expect_api_method='PUT',
            expect_api_url='/api/core/v2/namespaces/default/checks/test_check',
            expect_api_headers={
                'Authorization': 'Bearer token',
                'Content-type': 'application/json'
            },
            expect_api_payload={
                'metadata': {
                    'name': 'test_check',
                    'namespace': 'default'
                },
                'command': 'echo "test"',
                'subscriptions': ['switches'],
                'handlers': ['email'],
                'interval': 60,
                'publish': True,
                'timeout': 30,
                'ttl': 100,
                'stdin': False,
                'env_vars': ['RUBY_VERSION=2.5.0'],
                'low_flap_threshold': 20,
                'high_flap_threshold': 60,
                'runtime_assets': ['ruby-2.5.0'],
                'proxy_entity_name': 'switch-dc-01',
                'proxy_requests': {
                    'entity_attributes': ['entity.entity_class == "proxy"'],
                    'splay': True,
                    'splay_coverage': 90
                },
                'output_metric_format': 'nagios_perfdata',
                'output_metric_handlers': ['influx-db'],
                'round_robin': True
            },
        ),
        dict(
            name='Create Check on different namespace',
            params={
                'name': 'test_check',
                'namespace': 'testing_namespace',
                'command': 'echo "test"',
                'subscriptions': ['switches'],
                'handlers': ['email'],
                'interval': 60,
                'publish': True,
                'timeout': 30,
                'ttl': 100,
                'stdin': False,
                'env_vars': {'RUBY_VERSION': '2.5.0'},
                'low_flap_threshold': 20,
                'high_flap_threshold': 60,
                'runtime_assets': ['ruby-2.5.0'],
                'check_hooks': {},
                'proxy_entity_name': 'switch-dc-01',
                'proxy_entity_attributes': ['entity.entity_class == "proxy"'],
                'proxy_splay': True,
                'proxy_splay_coverage': 90,
                'output_metric_format': 'nagios_perfdata',
                'output_metric_handlers': ['influx-db'],
                'round_robin': True
            },
            expect_changed=True,
            expect_api_method='PUT',
            expect_api_url='/api/core/v2/namespaces/testing_namespace/checks/test_check',
            expect_api_headers={
                'Authorization': 'Bearer token',
                'Content-type': 'application/json'
            },
            expect_api_payload={
                'metadata': {
                    'name': 'test_check',
                    'namespace': 'testing_namespace'
                },
                'command': 'echo "test"',
                'subscriptions': ['switches'],
                'handlers': ['email'],
                'interval': 60,
                'publish': True,
                'timeout': 30,
                'ttl': 100,
                'stdin': False,
                'env_vars': ['RUBY_VERSION=2.5.0'],
                'low_flap_threshold': 20,
                'high_flap_threshold': 60,
                'runtime_assets': ['ruby-2.5.0'],
                'proxy_entity_name': 'switch-dc-01',
                'proxy_requests': {
                    'entity_attributes': ['entity.entity_class == "proxy"'],
                    'splay': True,
                    'splay_coverage': 90
                },
                'output_metric_format': 'nagios_perfdata',
                'output_metric_handlers': ['influx-db'],
                'round_robin': True
            },
        ),
        dict(
            name='Test idempotency',
            params={
                'name': 'test_check',
                'command': 'echo "test"',
                'subscriptions': ['switches'],
                'handlers': ['email'],
                'interval': 60,
                'publish': True,
                'timeout': 30,
                'ttl': 100,
                'stdin': False,
                'env_vars': {'RUBY_VERSION': '2.5.0'},
                'low_flap_threshold': 20,
                'high_flap_threshold': 60,
                'runtime_assets': ['ruby-2.5.0'],
                'check_hooks': {},
                'proxy_entity_name': 'switch-dc-01',
                'proxy_entity_attributes': ['entity.entity_class == "proxy"'],
                'proxy_splay': True,
                'proxy_splay_coverage': 90,
                'output_metric_format': 'nagios_perfdata',
                'output_metric_handlers': ['influx-db'],
                'round_robin': True
            },
            expect_changed=False,
            existing_object={
                'metadata': {
                    'name': 'test_check',
                    'namespace': 'default'
                },
                'command': 'echo "test"',
                'subscriptions': ['switches'],
                'handlers': ['email'],
                'interval': 60,
                'publish': True,
                'timeout': 30,
                'ttl': 100,
                'stdin': False,
                'env_vars': ['RUBY_VERSION=2.5.0'],
                'low_flap_threshold': 20,
                'high_flap_threshold': 60,
                'runtime_assets': ['ruby-2.5.0'],
                'proxy_entity_name': 'switch-dc-01',
                'proxy_requests': {
                    'entity_attributes': ['entity.entity_class == "proxy"'],
                    'splay': True,
                    'splay_coverage': 90
                },
                'output_metric_format': 'nagios_perfdata',
                'output_metric_handlers': ['influx-db'],
                'round_robin': True
            }
        ),
        dict(
            name='Update existing Check',
            params={
                'name': 'test_check',
                'command': 'echo "new-echo"',
                'subscriptions': ['new-subscriptions'],
                'handlers': ['new-handler'],
                'interval': 10,
                'publish': False,
                'timeout': 10,
                'ttl': 50,
                'stdin': True,
                'env_vars': {'NEW-ENV': 'test'},
                'low_flap_threshold': 10,
                'high_flap_threshold': 50,
                'runtime_assets': ['new-asset'],
                'check_hooks': {},
                'proxy_entity_name': 'new-entity',
                'proxy_entity_attributes': ['new.attribute == "new"'],
                'proxy_splay': True,
                'proxy_splay_coverage': 50,
                'output_metric_format': 'nagios_perfdata',
                'output_metric_handlers': ['new-handler'],
                'round_robin': False
            },
            expect_changed=True,
            expect_api_method='PUT',
            expect_api_url='/api/core/v2/namespaces/default/checks/test_check',
            expect_api_headers={
                'Authorization': 'Bearer token',
                'Content-type': 'application/json'
            },
            expect_api_payload={
                'metadata': {
                    'name': 'test_check',
                    'namespace': 'default'
                },
                'command': 'echo "new-echo"',
                'subscriptions': ['new-subscriptions'],
                'handlers': ['new-handler'],
                'interval': 10,
                'publish': False,
                'timeout': 10,
                'ttl': 50,
                'stdin': True,
                'env_vars': ['NEW-ENV=test'],
                'low_flap_threshold': 10,
                'high_flap_threshold': 50,
                'runtime_assets': ['new-asset'],
                'proxy_entity_name': 'new-entity',
                'proxy_requests': {
                    'entity_attributes': ['new.attribute == "new"'],
                    'splay': True,
                    'splay_coverage': 50
                },
                'output_metric_format': 'nagios_perfdata',
                'output_metric_handlers': ['new-handler'],
                'round_robin': False
            },
            existing_object={
                'metadata': {
                    'name': 'test_check',
                    'namespace': 'default'
                },
                'command': 'echo "test"',
                'subscriptions': ['switches'],
                'handlers': ['email'],
                'interval': 60,
                'publish': True,
                'timeout': 30,
                'ttl': 100,
                'stdin': False,
                'env_vars': ['RUBY_VERSION=2.5.0'],
                'low_flap_threshold': 20,
                'high_flap_threshold': 60,
                'runtime_assets': ['ruby-2.5.0'],
                'proxy_entity_name': 'switch-dc-01',
                'proxy_requests': {
                    'entity_attributes': ['entity.entity_class == "proxy"'],
                    'splay': True,
                    'splay_coverage': 90
                },
                'output_metric_format': 'nagios_perfdata',
                'output_metric_handlers': ['influx-db'],
                'round_robin': True
            }
        ),
        dict(
            name='Delete unexisting Check',
            params={
                'name': 'test_check',
                'state': 'absent'
            },
            expect_changed=False
        ),
        dict(
            name='Delete existing Check',
            params={
                'name': 'test_check',
                'state': 'absent'
            },
            expect_changed=True,
            expect_api_method='DELETE',
            expect_api_url='/api/core/v2/namespaces/default/checks/test_check',
            expect_api_headers={
                'Authorization': 'Bearer token',
            },
            existing_object={
                'metadata': {
                    'name': 'test_check',
                    'namespace': 'default'
                },
                'command': 'echo "test"',
                'subscriptions': ['switches'],
                'handlers': ['email'],
                'interval': 60,
                'publish': True,
                'timeout': 30,
                'ttl': 100,
                'stdin': False,
                'env_vars': ['RUBY_VERSION=2.5.0'],
                'low_flap_threshold': 20,
                'high_flap_threshold': 60,
                'runtime_assets': ['ruby-2.5.0'],
                'proxy_entity_name': 'switch-dc-01',
                'proxy_requests': {
                    'entity_attributes': ['entity.entity_class == "proxy"'],
                    'splay': True,
                    'splay_coverage': 90
                },
                'output_metric_format': 'nagios_perfdata',
                'output_metric_handlers': ['influx-db'],
                'round_robin': True
            }
        ),
        dict(
            name='(check) Create Check',
            params={
                'name': 'test_check',
                'command': 'echo "test"',
                'subscriptions': ['switches'],
                'handlers': ['email'],
                'interval': 60,
                'publish': True,
                'timeout': 30,
                'ttl': 100,
                'stdin': False,
                'env_vars': {'RUBY_VERSION': '2.5.0'},
                'low_flap_threshold': 20,
                'high_flap_threshold': 60,
                'runtime_assets': ['ruby-2.5.0'],
                'check_hooks': {},
                'proxy_entity_name': 'switch-dc-01',
                'proxy_entity_attributes': ['entity.entity_class == "proxy"'],
                'proxy_splay': True,
                'proxy_splay_coverage': 90,
                'output_metric_format': 'nagios_perfdata',
                'output_metric_handlers': ['influx-db'],
                'round_robin': True
            },
            check_mode=True,
            expect_changed=True,
        ),
        dict(
            name='(check) Update Check',
            params={
                'name': 'test_check',
                'command': 'echo "new-echo"',
                'subscriptions': ['new-subscriptions'],
                'handlers': ['new-handler'],
                'interval': 10,
                'publish': False,
                'timeout': 10,
                'ttl': 50,
                'stdin': True,
                'env_vars': {'NEW-ENV': 'test'},
                'low_flap_threshold': 10,
                'high_flap_threshold': 50,
                'runtime_assets': ['new-asset'],
                'check_hooks': {},
                'proxy_entity_name': 'new-entity',
                'proxy_entity_attributes': ['new.attribute == "new"'],
                'proxy_splay': True,
                'proxy_splay_coverage': 50,
                'output_metric_format': 'nagios_perfdata',
                'output_metric_handlers': ['new-handler'],
                'round_robin': False
            },
            check_mode=True,
            expect_changed=True,
            existing_object={
                'metadata': {
                    'name': 'test_check',
                    'namespace': 'default'
                },
                'command': 'echo "test"',
                'subscriptions': ['switches'],
                'handlers': ['email'],
                'interval': 60,
                'publish': True,
                'timeout': 30,
                'ttl': 100,
                'stdin': False,
                'env_vars': ['RUBY_VERSION=2.5.0'],
                'low_flap_threshold': 20,
                'high_flap_threshold': 60,
                'runtime_assets': ['ruby-2.5.0'],
                'proxy_entity_name': 'switch-dc-01',
                'proxy_requests': {
                    'entity_attributes': ['entity.entity_class == "proxy"'],
                    'splay': True,
                    'splay_coverage': 90
                },
                'output_metric_format': 'nagios_perfdata',
                'output_metric_handlers': ['influx-db'],
                'round_robin': True
            }
        ),
        dict(
            name='(check) Update Check idempotency',
            params={
                'name': 'test_check',
                'command': 'echo "test"',
                'subscriptions': ['switches'],
                'handlers': ['email'],
                'interval': 60,
                'publish': True,
                'timeout': 30,
                'ttl': 100,
                'stdin': False,
                'env_vars': {'RUBY_VERSION': '2.5.0'},
                'low_flap_threshold': 20,
                'high_flap_threshold': 60,
                'runtime_assets': ['ruby-2.5.0'],
                'check_hooks': {},
                'proxy_entity_name': 'switch-dc-01',
                'proxy_entity_attributes': ['entity.entity_class == "proxy"'],
                'proxy_splay': True,
                'proxy_splay_coverage': 90,
                'output_metric_format': 'nagios_perfdata',
                'output_metric_handlers': ['influx-db'],
                'round_robin': True
            },
            check_mode=True,
            expect_changed=False,
            existing_object={
                'metadata': {
                    'name': 'test_check',
                    'namespace': 'default'
                },
                'command': 'echo "test"',
                'subscriptions': ['switches'],
                'handlers': ['email'],
                'interval': 60,
                'publish': True,
                'timeout': 30,
                'ttl': 100,
                'stdin': False,
                'env_vars': ['RUBY_VERSION=2.5.0'],
                'low_flap_threshold': 20,
                'high_flap_threshold': 60,
                'runtime_assets': ['ruby-2.5.0'],
                'proxy_entity_name': 'switch-dc-01',
                'proxy_requests': {
                    'entity_attributes': ['entity.entity_class == "proxy"'],
                    'splay': True,
                    'splay_coverage': 90
                },
                'output_metric_format': 'nagios_perfdata',
                'output_metric_handlers': ['influx-db'],
                'round_robin': True
            }
        ),
        dict(
            name='(check) Delete unexisting Check',
            params={
                'name': 'test_check',
                'state': 'absent',
            },
            check_mode=True,
            expect_changed=False,
        ),
        dict(
            name='(check) Delete existing Check',
            params={
                'name': 'test_check',
                'state': 'absent',
            },
            check_mode=True,
            expect_changed=True,
            existing_object={
                'metadata': {
                    'name': 'test_check',
                    'namespace': 'default'
                },
                'command': 'echo "test"',
                'subscriptions': ['switches'],
                'handlers': ['email'],
                'interval': 60,
                'publish': True,
                'timeout': 30,
                'ttl': 100,
                'stdin': False,
                'env_vars': ['RUBY_VERSION=2.5.0'],
                'low_flap_threshold': 20,
                'high_flap_threshold': 60,
                'runtime_assets': ['ruby-2.5.0'],
                'proxy_entity_name': 'switch-dc-01',
                'proxy_requests': {
                    'entity_attributes': ['entity.entity_class == "proxy"'],
                    'splay': True,
                    'splay_coverage': 90
                },
                'output_metric_format': 'nagios_perfdata',
                'output_metric_handlers': ['influx-db'],
                'round_robin': True
            }
        ),
    ]

    @pytest.mark.parametrize('test_data', matrix, ids=generate_name)
    def test_module(self, test_data):
        self.run_test_case(test_data)
