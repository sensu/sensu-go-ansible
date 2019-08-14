import pytest

from ansible_collections.sensu.sensu_go.plugins.modules import sensu_go_filter
from ansible_collections.sensu.sensu_go.test.unit.modules.common.utils import ModuleTestCase, generate_name
from ansible_collections.sensu.sensu_go.test.unit.modules.common.sensu_go_object import TestSensuGoObjectBase


class TestSensuFilterModule(ModuleTestCase, TestSensuGoObjectBase):
    module = sensu_go_filter

    @pytest.mark.parametrize('test_data', [
        dict(
            name='Test unreachable URL',
            params={
                'name': 'test_filter',
                'action': 'allow',
                'expressions': ['event.check.occurrences == 1']
            },
            is_http_error=True,
            expect_failed=True,
            expect_msg='authentication failed: unreachable'
        ),
        dict(
            name='Create Filter',
            params={
                'name': 'test_filter',
                'action': 'allow',
                'expressions': ['event.check.occurrences == 1'],
            },
            expect_changed=True,
            expect_api_method='PUT',
            expect_api_url='/api/core/v2/namespaces/default/filters/test_filter',
            expect_api_headers={
                'Authorization': 'Bearer token',
                'Content-type': 'application/json'
            },
            expect_api_payload={
                'metadata': {
                    'name': 'test_filter',
                    'namespace': 'default'
                },
                'expressions': ['event.check.occurrences == 1']
            },
        ),
        dict(
            name='Create Filter on different namespace',
            params={
                'name': 'test_filter',
                'namespace': 'testing_namespace',
                'action': 'allow',
                'expressions': ['event.check.occurrences == 1'],
            },
            expect_changed=True,
            expect_api_method='PUT',
            expect_api_url='/api/core/v2/namespaces/testing_namespace/filters/test_filter',
            expect_api_headers={
                'Authorization': 'Bearer token',
                'Content-type': 'application/json'
            },
            expect_api_payload={
                'metadata': {
                    'name': 'test_filter',
                    'namespace': 'testing_namespace'
                },
                'expressions': ['event.check.occurrences == 1']
            },
        ),
        dict(
            name='Create Filter without expressions',
            params={
                'name': 'test_filter',
                'action': 'allow',
            },
            expect_failed=True,
            expect_msg='state is present but all of the following are missing: expressions'
        ),
        dict(
            name='Test idempotency',
            params={
                'name': 'test_filter',
                'action': 'allow',
                'expressions': ['event.check.occurrences == 1'],
                'runtime_assets': []
            },
            expect_changed=False,
            existing_object={
                'metadata': {
                    'name': 'test_filter',
                    'namespace': 'default'
                },
                'action': 'allow',
                'expressions': ['event.check.occurrences == 1'],
                'runtime_assets': []
            }
        ),
        dict(
            name='Update existing Filter',
            params={
                'name': 'test_filter',
                'action': 'deny',
                'expressions': ['new.expression == update'],
                'runtime_assets': ['new-asset']
            },
            expect_changed=True,
            expect_api_method='PUT',
            expect_api_url='/api/core/v2/namespaces/default/filters/test_filter',
            expect_api_headers={
                'Authorization': 'Bearer token',
                'Content-type': 'application/json'
            },
            expect_api_payload={
                'metadata': {
                    'name': 'test_filter',
                    'namespace': 'default'
                },
                'action': 'deny',
                'expressions': ['new.expression == update'],
                'runtime_assets': ['new-asset']
            },
            existing_object={
                'metadata': {
                    'name': 'test_filter',
                    'namespace': 'default'
                },
                'action': 'allow',
                'expressions': ['event.check.occurrences == 1'],
                'runtime_assets': ['ruby-2.4.4']
            }
        ),
        dict(
            name='Delete Filter',
            params={
                'name': 'test_filter',
                'state': 'absent'
            },
            expect_changed=False
        ),
        dict(
            name='Delete existing Filter',
            params={
                'name': 'test_filter',
                'state': 'absent'
            },
            expect_changed=True,
            expect_api_method='DELETE',
            expect_api_url='/api/core/v2/namespaces/default/filters/test_filter',
            expect_api_headers={
                'Authorization': 'Bearer token',
            },
            existing_object={
                'metadata': {
                    'name': 'test_filter',
                    'namespace': 'default'
                },
                'action': 'allow',
                'expressions': ['event.check.occurrences == 1'],
                'runtime_assets': ['ruby-2.4.4']
            }
        ),
        dict(
            name='(check) Create Filter',
            params={
                'name': 'test_filter',
                'action': 'allow',
                'expressions': ['event.check.occurrences == 1'],
                'runtime_assets': ['ruby-2.4.4']
            },
            check_mode=True,
            expect_changed=True,
        ),
        dict(
            name='(check) Update Filter',
            params={
                'name': 'test_filter',
                'action': 'deny',
                'expressions': ['new.expression == update'],
                'runtime_assets': ['new-asset']
            },
            check_mode=True,
            expect_changed=True,
            existing_object={
                'metadata': {
                    'name': 'test_filter',
                    'namespace': 'default'
                },
                'action': 'deny',
                'expressions': ['event.check.occurrences == 1'],
                'runtime_assets': ['ruby-2.4.4']
            }
        ),
        dict(
            name='(check) Update Filter idempotency',
            params={
                'name': 'test_filter',
                'state': 'present',
                'action': 'allow',
                'expressions': ['event.check.occurrences == 1'],
                'runtime_assets': ['ruby-2.4.4']
            },
            check_mode=True,
            expect_changed=False,
            existing_object={
                'metadata': {
                    'name': 'test_filter',
                    'namespace': 'default'
                },
                'action': 'allow',
                'expressions': ['event.check.occurrences == 1'],
                'runtime_assets': ['ruby-2.4.4']
            }
        ),
        dict(
            name='(check) Delete Filter',
            params={
                'name': 'test_filter',
                'state': 'absent'
            },
            check_mode=True,
            expect_changed=False,
        ),
        dict(
            name='(check) Delete existing Filter',
            params={
                'name': 'test_filter',
                'state': 'absent',
            },
            check_mode=True,
            expect_changed=True,
            existing_object={
                'metadata': {
                    'name': 'test_filter',
                    'namespace': 'default'
                },
                'action': 'allow',
                'expressions': ['event.check.occurrences == 1'],
                'runtime_assets': ['ruby-2.4.4']
            }
        ),
    ], ids=generate_name)
    def test_filter_module(self, test_data):
        self.run_test_case(test_data)
