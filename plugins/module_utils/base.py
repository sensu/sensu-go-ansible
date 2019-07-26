# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Paul Arthur <paul.arthur@flowerysong.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.module_utils._text import to_native, to_text
from ansible.module_utils.basic import env_fallback
from ansible.module_utils.urls import open_url
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError

import json
import os


def sensu_argument_spec():
    return dict(
        user=dict(
            default='admin',
            fallback=(env_fallback, ['SENSU_USER']),
        ),
        password=dict(
            default='P@ssw0rd!',
            no_log=True,
            fallback=(env_fallback, ['SENSU_PASSWORD']),
        ),
        url=dict(
            default='http://localhost:8080',
            fallback=(env_fallback, ['SENSU_BACKEND_URL']),
        ),
        namespace=dict(
            default='default',
        ),
    )


class AnsibleSensuClient():
    def __init__(self, module):
        self.module = module
        self.params = module.params
        self.url = self.params['url'].rstrip('/')
        self.user = self.params['user']
        self.password = self.params['password']
        self.namespace = self.params['namespace']

        try:
            auth = open_url(
                '{0}/auth'.format(self.url),
                url_username=self.user,
                url_password=self.password,
                force_basic_auth=True,
            )
        except (HTTPError, URLError) as e:
            module.fail_json(msg='authentication failed: {0}'.format(e.reason))
        parsed = json.loads(auth.read())

        self.token = parsed['access_token']

    def _open_url(self, path, method, data=None):
        if self.namespace:
            url = '{0}/api/core/v2/namespaces/{1}{2}'.format(self.url, self.namespace, path)
        else:
            url = '{0}/api/core/v2{1}'.format(self.url, path)

        headers = dict(
            Authorization='Bearer {0}'.format(self.token),
        )
        if data:
            headers['Content-type'] = 'application/json'

        return open_url(url, headers=headers, method=method, data=self.module.jsonify(data))

    def get(self, path):
        try:
            result = self._open_url(path, method='GET')
        except HTTPError as e:
            if e.code == 404:
                return {}
            self.module.fail_json(msg='get failed: {0}'.format(e.reason))
        return json.loads(result.read())

    def put(self, path, data):
        try:
            result = self._open_url(path, method='PUT', data=data)
        except HTTPError as e:
            self.module.fail_json(msg='put failed: {0}'.format(e.reason))

    def delete(self, path):
        try:
            result = self._open_url(path, method='DELETE')
        except HTTPError as e:
            if e.code == 404:
                return False
            self.module.fail_json(msg='delete failed: {0}'.format(e.reason))
        return True


class SensuObject():
    def __init__(self, module):
        self.module = module
        self.client = AnsibleSensuClient(module)
        self.params = module.params
        self.payload = {
            'metadata': {
                'name': self.params['name'],
                'namespace': self.params['namespace'],
            },
        }
        for key in ('labels', 'annotations'):
            if self.params[key]:
                self.payload['metadata'][key] = SensuObject._clean_tags(self.params[key])

    @staticmethod
    def _clean_tags(tags):
        # Sensu metadata must always be strings
        ret = {}
        for key in tags:
            ret[key] = str(tags[key])
        return ret

    @staticmethod
    def argument_spec():
        argspec = sensu_argument_spec()
        argspec.update(
            dict(
                state=dict(
                    default='present',
                    choices=['present', 'absent'],
                ),
                name=dict(
                    required=True,
                ),
                labels=dict(
                    type='dict',
                    default={},
                ),
                annotations=dict(
                    type='dict',
                    default={},
                ),
            )
        )
        return argspec

    # Some places where it would seem natural to take a dict instead take
    # a list of single-key dicts. This is a convenience function that transforms
    # {key1: val1, key2: val2} into [{key1: val1}, {key2: val2}]
    def param_dict_to_payload_list(self, key):
        if self.params[key]:
            self.payload[key] = [{k, v} for k, v in self.params[key].items()]
            self.payload[key].sort()

    def param_dict_to_payload_kv_list(self, key):
        if self.params[key]:
            self.payload[key] = [k + '=' + v for k, v in self.params[key].items()]
            self.payload[key].sort()

    def delete(self):
        return self.client.delete(self.path)

    def get(self, cached=True):
        if not cached or not hasattr(self, 'server_object'):
            self.server_object = self.client.get(self.path)
        return self.server_object

    def compare(self):
        for key in self.payload:
            if self.payload[key] != self.server_object.get(key):
                return False
        return True

    def update(self):
        self.client.put(self.path, self.payload)

    def reconcile(self):
        result = self.get()
        changed = False

        if self.params['state'] == 'absent':
            if result:
                if self.module.check_mode:
                    changed = True
                else:
                    changed = self.delete()

        elif not self.compare():
            changed = True
            if self.module.check_mode:
                result = self.payload
            else:
                self.update()
                result = self.get(False)

        return({'changed': changed, 'object': result})
