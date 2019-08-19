from __future__ import absolute_import, division, print_function
__metaclass__ = type

import re
import json
import copy

import pytest

from .utils import ModuleTestCase, set_module_args, AnsibleExitJson, patch


class TestSensuGoObjectInfoBase(object):
    module = None
    default_test_case = dict(
        params={'url': 'http://test:8080'},  # Module input parameters
        expect_result_key=None,  # key in module result
        check_mode=False,  # Module check mode
        expect_api_url=None,  # expected api url
        existing_object=None  # params of existing object on API
    )

    def run_test_case(self, test_case):
        test_case = self._extend_default_test_case(test_case)
        with patch('ansible_collections.sensu.sensu_go.plugins.module_utils.base.open_url') as open_url_mock:
            self._configure_mock(open_url_mock, test_case)
            # _ansible_* keys are added here, we deepcopy it so it doesn't mess with our test case
            set_module_args(self._prepare_input_params(copy.deepcopy(test_case)))

            with pytest.raises(AnsibleExitJson) as context:
                self.module.main()
            result = context.value.args[0]

            assert result[test_case['expect_result_key']] == test_case['expect_result'], \
                '{} != {}'.format(result[test_case['expect_result_key']], test_case['expect_result'])
            if len(open_url_mock.call_args_list) == 2:
                api_url = open_url_mock.call_args_list[1][0][0]
                kwrd_args = open_url_mock.call_args_list[1][1]
                assert kwrd_args['method'] == 'GET', 'only GET method expected for info modules'
                assert api_url == self._build_url(test_case), '{} != {}'.format(api_url, self._build_url(test_case))
            elif len(open_url_mock.call_args_list) == 1:
                assert False, 'no API call was performed'
            else:
                assert False, 'too many API calls were performed'
            assert result['changed'] is False, 'info module should not change anything'

    def _extend_default_test_case(self, test_case):
        merged_test_case = self.default_test_case.copy()
        merged_test_case.update(test_case)
        merged_test_case['params']['url'] = (test_case['params'].get('url') or
                                             self.default_test_case['params']['url'])
        return merged_test_case

    def _configure_mock(self, mock, test_case):
        def config():
            auth_response = '{"access_token": "token"}'
            if test_case['existing_object'] is not None:
                # In the case of testing update we return 'existing_object' from API
                payload = json.dumps(test_case['existing_object'])
                return {'return_value.read.side_effect': [auth_response, payload]}
            return {'return_value.read.return_value': auth_response}
        mock.configure_mock(**config())
        return mock

    def _build_url(self, test_case):
        has_hostname = re.match('(?:http|ftp|https)://', test_case['expect_api_url'])
        if not has_hostname:
            return '{}{}'.format(test_case['params']['url'], test_case['expect_api_url'])
        return test_case['expect_api_url']

    def _prepare_input_params(self, test_case):
        if test_case['check_mode']:
            test_case['params']['_ansible_check_mode'] = test_case['check_mode']
        return test_case['params']
