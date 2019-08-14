import pytest

from ansible_collections.sensu.sensu_go.plugins.modules import sensu_go_mutator
from ansible_collections.sensu.sensu_go.test.unit.modules.common.utils import ModuleTestCase, generate_name
from ansible_collections.sensu.sensu_go.test.unit.modules.common.sensu_go_object import TestSensuGoObjectBase


class TestSensuMutatorModule(ModuleTestCase, TestSensuGoObjectBase):
    module = sensu_go_mutator

    @pytest.mark.parametrize('test_data', [
        dict(
            name='Test unreachable URL',
            params={
                'name': 'test_mutator',
                'command': 'echo "test"',
                'timeout': 30,
                'env_vars': {'RUBY_VERSION': '2.5.0'},
                'runtime_assets': ["ruby-2.5.0"]
            },
            is_http_error=True,
            expect_failed=True,
            expect_msg='authentication failed: unreachable'
        ),
        dict(
            name='Create Mutator',
            params={
                'name': 'test_mutator',
                'command': 'echo "test"',
                'timeout': 30,
                'env_vars': {'RUBY_VERSION': '2.5.0'},
                'runtime_assets': ["ruby-2.5.0"]
            },
            expect_changed=True,
            expect_api_method='PUT',
            expect_api_url='/api/core/v2/namespaces/default/mutators/test_mutator',
            expect_api_headers={
                'Authorization': 'Bearer token',
                'Content-type': 'application/json'
            },
            expect_api_payload={
                'metadata': {
                    'name': 'test_mutator',
                    'namespace': 'default'
                },
                'command': 'echo "test"',
                'timeout': 30,
                'env_vars': ['RUBY_VERSION=2.5.0'],
                'runtime_assets': ["ruby-2.5.0"]
            },
        ),
        dict(
            name='Create Mutator on different namespace',
            params={
                'name': 'test_mutator',
                'namespace': 'testing_namespace',
                'command': 'echo "test"',
                'timeout': 30,
                'env_vars': {'RUBY_VERSION': '2.5.0'},
                'runtime_assets': ["ruby-2.5.0"]
            },
            expect_changed=True,
            expect_api_method='PUT',
            expect_api_url='/api/core/v2/namespaces/testing_namespace/mutators/test_mutator',
            expect_api_headers={
                'Authorization': 'Bearer token',
                'Content-type': 'application/json'
            },
            expect_api_payload={
                'metadata': {
                    'name': 'test_mutator',
                    'namespace': 'testing_namespace'
                },
                'command': 'echo "test"',
                'timeout': 30,
                'env_vars': ['RUBY_VERSION=2.5.0'],
                'runtime_assets': ["ruby-2.5.0"]
            },
        ),
        dict(
            name='Test idempotency',
            params={
                'name': 'test_mutator',
                'command': 'echo "test"',
                'timeout': 30,
                'env_vars': {'RUBY_VERSION': '2.5.0'},
                'runtime_assets': ["ruby-2.5.0"]
            },
            expect_changed=False,
            existing_object={
                'metadata': {
                    'name': 'test_mutator',
                    'namespace': 'default'
                },
                'command': 'echo "test"',
                'timeout': 30,
                'env_vars': ['RUBY_VERSION=2.5.0'],
                'runtime_assets': ["ruby-2.5.0"]
            }
        ),
        dict(
            name='Update existing Mutator',
            params={
                'name': 'test_mutator',
                'command': 'echo "new-test"',
                'timeout': 60,
                'env_vars': {'NEW-ENV': 'test'},
                'runtime_assets': ["new-asset"]
            },
            expect_changed=True,
            expect_api_method='PUT',
            expect_api_url='/api/core/v2/namespaces/default/mutators/test_mutator',
            expect_api_headers={
                'Authorization': 'Bearer token',
                'Content-type': 'application/json'
            },
            expect_api_payload={
                'metadata': {
                    'name': 'test_mutator',
                    'namespace': 'default'
                },
                'command': 'echo "new-test"',
                'timeout': 60,
                'env_vars': ['NEW-ENV=test'],
                'runtime_assets': ["new-asset"]
            },
            existing_object={
                'metadata': {
                    'name': 'test_mutator',
                    'namespace': 'default'
                },
                'command': 'echo "test"',
                'timeout': 30,
                'env_vars': ['RUBY_VERSION=2.5.0'],
                'runtime_assets': ["ruby-2.5.0"]
            }
        ),
        dict(
            name='Delete unexisting Check',
            params={
                'name': 'test_mutator',
                'state': 'absent'
            },
            expect_changed=False
        ),
        dict(
            name='Delete existing Mutator',
            params={
                'name': 'test_mutator',
                'state': 'absent'
            },
            expect_changed=True,
            expect_api_method='DELETE',
            expect_api_url='/api/core/v2/namespaces/default/mutators/test_mutator',
            expect_api_headers={
                'Authorization': 'Bearer token',
            },
            existing_object={
                'metadata': {
                    'name': 'test_mutator',
                    'namespace': 'default'
                },
                'command': 'echo "test"',
                'timeout': 30,
                'env_vars': ['RUBY_VERSION=2.5.0'],
                'runtime_assets': ["ruby-2.5.0"]
            }
        ),
        dict(
            name='(check) Create Mutator',
            params={
                'name': 'test_mutator',
                'command': 'echo "test"',
                'timeout': 30,
                'env_vars': {'RUBY_VERSION': '2.5.0'},
                'runtime_assets': ["ruby-2.5.0"]
            },
            check_mode=True,
            expect_changed=True,
        ),
        dict(
            name='(check) Update Mutator',
            params={
                'name': 'test_mutator',
                'command': 'echo "new-test"',
                'timeout': 60,
                'env_vars': {'NEW-ENV': 'test'},
                'runtime_assets': ["new-asset"]
            },
            check_mode=True,
            expect_changed=True,
            existing_object={
                'metadata': {
                    'name': 'test_mutator',
                    'namespace': 'default'
                },
                'command': 'echo "test"',
                'timeout': 30,
                'env_vars': ['RUBY_VERSION=2.5.0'],
                'runtime_assets': ["ruby-2.5.0"]
            }
        ),
        dict(
            name='(check) Update Mutator idempotency',
            params={
                'name': 'test_mutator',
                'command': 'echo "test"',
                'timeout': 30,
                'env_vars': {'RUBY_VERSION': '2.5.0'},
                'runtime_assets': ["ruby-2.5.0"]
            },
            check_mode=True,
            expect_changed=False,
            existing_object={
                'metadata': {
                    'name': 'test_mutator',
                    'namespace': 'default'
                },
                'command': 'echo "test"',
                'timeout': 30,
                'env_vars': ['RUBY_VERSION=2.5.0'],
                'runtime_assets': ["ruby-2.5.0"]
            }
        ),
        dict(
            name='(check) Delete unexisting Mutator',
            params={
                'name': 'test_mutator',
                'state': 'absent'
            },
            check_mode=True,
            expect_changed=False,
        ),
        dict(
            name='(check) Delete existing Mutator',
            params={
                'name': 'test_mutator',
                'state': 'absent',
            },
            check_mode=True,
            expect_changed=True,
            existing_object={
                'metadata': {
                    'name': 'test_mutator',
                    'namespace': 'default'
                },
                'command': 'echo "test"',
                'timeout': 30,
                'env_vars': ['RUBY_VERSION=2.5.0'],
                'runtime_assets': ["ruby-2.5.0"]
            }
        ),
    ], ids=generate_name)
    def test_mutator_module(self, test_data):
        self.run_test_case(test_data)
