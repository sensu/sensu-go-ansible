import json

from unittest.mock import patch
from ansible_collections.sensu.sensu_go.test.unit.modules.common.utils import ModuleTestCase, \
    set_module_args, AnsibleFailJson, AnsibleExitJson
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError

import pytest


class TestSensuGoObjectBase(object):
    module = None
    default_test_case = dict(
        params=None,  # Module input parameters
        is_http_error=False,
        expect_failed=False,
        expect_msg=None,
        expect_changed=False,
        expect_api_method='GET',
        expect_api_url=None,
        expect_api_headers=None
    )

    def run_test_case(self, test_case):
        test_case = self._extend_default_test_case(test_case)
        with patch('ansible_collections.sensu.sensu_go.plugins.module_utils.base.open_url') as open_url_mock:
            self._configure_mock(open_url_mock, test_case)
            set_module_args(test_case['params'].copy())

            with pytest.raises(self._get_exit_class(test_case)) as context:
                self.module.main()
            result = context.value.args[0]
            self._assert_module_output(result, test_case)

            if test_case['params'].get('state', 'present') == 'present':
                # If there are more than 2 calls and state is present, we have a PUT method
                if len(open_url_mock.call_args_list) > 2:
                    self._assert_put(open_url_mock, test_case)
                elif test_case['expect_api_url'] is not None:
                    assert False, 'no API call was performed'

    def _extend_default_test_case(self, test_case):
        merged_test_case = self.default_test_case.copy()
        merged_test_case.update(test_case)
        return merged_test_case

    def _configure_mock(self, mock, test_case):
        if test_case['is_http_error']:
            mock.configure_mock(**{'side_effect': URLError('unreachable')})
        else:
            mock.configure_mock(**{'return_value.read.return_value': '{"access_token": "token"}'})
        return mock

    def _assert_module_output(self, result, test_case):
        assert result.get('failed', False) is test_case['expect_failed']
        assert result.get('msg', None) == test_case['expect_msg']
        assert result.get('changed', False) is test_case['expect_changed']

    def _assert_put(self, open_url_mock, test_case):
        open_url_call = open_url_mock.call_args_list[2]
        url = open_url_call[0][0]
        headers = open_url_call[1]['headers']
        method = open_url_call[1]['method']
        data = json.loads(open_url_call[1]['data'])

        expected_data = self._prepare_expected_data(test_case['params'].copy())
        assert data == expected_data
        assert method == test_case['expect_api_method']
        assert url == test_case['expect_api_url']
        assert headers == test_case['expect_api_headers']

    def _prepare_expected_data(self, params):
        [params.pop(k, None) for k in ('url', 'state')]
        params['metadata'] = {
            'namespace': 'default',
            'name': params.pop('name')
        }
        return params

    def _get_exit_class(self, test_case):
        if test_case.get('expect_failed', False):
            return AnsibleFailJson
        return AnsibleExitJson
