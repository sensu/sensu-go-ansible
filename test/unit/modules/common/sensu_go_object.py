from __future__ import absolute_import, division, print_function
__metaclass__ = type

import re
import json
import copy

import pytest

from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError

from .utils import (
    set_module_args, AnsibleFailJson, AnsibleExitJson, patch
)


class TestSensuGoObjectBase(object):
    module = None
    default_test_case = dict(
        params={'url': 'http://test:8080'},  # Module input parameters
        check_mode=False,  # Module check mode
        is_http_error=False,  # Indicates whether to throw a HTTPError or not
        expect_failed=False,  # expected value of failed key returned by module
        expect_msg=None,  # expected value of msg key returned by module
        expect_changed=False,  # expected value of changed key returned by module
        expect_api_method='PUT',  # expected HTTP method
        expect_api_url=None,  # expected api url
        expect_api_headers=None,  # dict of expected headers on API call
        existing_object={}  # params of existing object on API
    )

    def run_test_case(self, test_case):
        test_case = self._extend_default_test_case(test_case)
        with patch('ansible_collections.sensu.sensu_go.plugins.module_utils.base.open_url') as open_url_mock:
            self._configure_mock(open_url_mock, test_case)
            # _ansible_* keys are added here, we deepcopy it so it doesn't mess with our test case
            set_module_args(self._prepare_input_params(copy.deepcopy(test_case)))

            with pytest.raises(self._get_exit_class(test_case)) as context:
                self.module.main()
            result = context.value.args[0]
            self._assert_module_output(result, test_case)

            if test_case['check_mode']:
                assert open_url_mock.call_count == 2  # One for auth and one for fetching object

            if len(open_url_mock.call_args_list) > 2:
                # If there are more than 2 calls we have PUT or DELETE
                state = test_case['params'].get('state', 'present')
                if state == 'present':
                    self._assert_put(open_url_mock, test_case)
                elif state == 'absent':
                    self._assert_delete(open_url_mock, test_case)
            elif test_case['expect_api_url'] is not None:
                assert False, 'no API call was performed'

    def _extend_default_test_case(self, test_case):
        merged_test_case = self.default_test_case.copy()
        merged_test_case.update(test_case)
        merged_test_case['params']['url'] = (test_case['params'].get('url') or
                                             self.default_test_case['params']['url'])
        return merged_test_case

    def _configure_mock(self, mock, test_case):
        def config():
            auth_response = '{"access_token": "token"}'
            if test_case['existing_object']:
                # In the case of testing update we return 'existing_object' from API
                payload = json.dumps(test_case['existing_object'])
                return {'return_value.read.side_effect': [auth_response, payload, payload]}
            elif test_case['params'].get('state', 'present') == 'absent':
                # If the state is absent and 'existing_object' is not present,
                # we want empty response by default
                return {'return_value.read.side_effect': [auth_response, '{}']}
            return {'return_value.read.return_value': auth_response}

        if test_case['is_http_error']:
            mock.configure_mock(**{'side_effect': URLError('unreachable')})
        else:
            mock.configure_mock(**config())
        return mock

    def _assert_module_output(self, result, test_case):
        assert result.get('failed', False) is test_case['expect_failed']
        assert result.get('msg', None) == test_case['expect_msg']
        assert result.get('changed', False) is test_case['expect_changed']

    def _assert_put(self, open_url_mock, test_case):
        url, headers, method, data = self._parse_mock_call(open_url_mock.call_args_list[2])
        # Merge expected params on top of API params so we get all the default values
        expected_data = copy.deepcopy(data)
        expected_data.update(test_case['expect_api_payload'].copy())

        assert data == expected_data
        assert method == test_case['expect_api_method']
        assert url == self._build_url(test_case)
        assert headers == test_case['expect_api_headers']

    def _assert_delete(self, open_url_mock, test_case):
        url, headers, method, data = self._parse_mock_call(open_url_mock.call_args_list[2])
        assert data is None
        assert method == test_case['expect_api_method']
        assert url == self._build_url(test_case)
        assert headers == test_case['expect_api_headers']

    def _build_url(self, test_case):
        has_hostname = re.match('(?:http|ftp|https)://', test_case['expect_api_url'])
        if not has_hostname:
            return '{}{}'.format(test_case['params']['url'], test_case['expect_api_url'])
        return test_case['expect_api_url']

    def _parse_mock_call(self, mock_call):
        url = mock_call[0][0]
        headers = mock_call[1]['headers']
        method = mock_call[1]['method']
        data = json.loads(mock_call[1]['data'])
        return url, headers, method, data

    def _prepare_input_params(self, test_case):
        if test_case['check_mode']:
            test_case['params']['_ansible_check_mode'] = test_case['check_mode']
        return test_case['params']

    def _get_exit_class(self, test_case):
        if test_case['expect_failed']:
            return AnsibleFailJson
        return AnsibleExitJson
