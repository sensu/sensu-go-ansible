#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Paul Arthur <paul.arthur@flowerysong.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
module: sensu_go_user
author: "Paul Arthur (@flowerysong)"
short_description: Manages Sensu users
description:
  - 'For more information, refer to the Sensu documentation: U(https://docs.sensu.io/sensu-go/latest/reference/users/)'
extends_documentation_fragment:
  - flowerysong.sensu_go.base
options:
  action:
    description:
      - Filter action.
    choices: [ 'allow', 'deny' ]
    default: allow
'''

EXAMPLES = '''
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import open_url
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError

from ansible_collections.flowerysong.sensu_go.plugins.module_utils.base import sensu_argument_spec, AnsibleSensuClient


def main():
    argspec = sensu_argument_spec()
    argspec.update(dict(
        state=dict(
            default='present',
            choices=['present', 'absent'],
        ),
        name=dict(
            required=True,
        ),
        user_password=dict(
            no_log=True,
        ),
        groups=dict(
            type='list',
            default=[],
        ),
        purge_groups=dict(
            type='bool',
            default=True,
        ),
    ))

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
    )

    client = AnsibleSensuClient(module)
    client.namespace = None

    params = module.params
    user_path = '/users/{0}'.format(params['name'])

    user = client.get(user_path)
    changed = False

    if params['state'] == 'absent':
        if user and not user['disabled']:
            changed = True
            if not module.check_mode:
                client.delete(user_path)
                user = client.get(user_path)
        module.exit_json(changed=changed, user=user)

    if not user:
        payload = {
            'username': params['name'],
            'groups': params['groups'],
            'password': params['user_password'],
            'disabled': False,
        }

        if module.check_mode:
            user = payload
        else:
            client.put(user_path, payload)
            user = client.get(user_path)

        module.exit_json(changed=True, user=user)


    if user['disabled']:
        changed = True
        if not module.check_mode:
            client.put('{0}/reinstate'.format(user_path), {})

    groups = params['groups']
    if params['purge_groups']:
        for group in user.get('groups', []):
            if group not in groups:
                changed = True
                if not module.check_mode:
                    client.delete('{0}/groups/{1}'.format(user_path, group))

    for group in groups:
        if group not in user.get('groups', []):
            changed = True
            if not module.check_mode:
                client.put('{0}/groups/{1}'.format(user_path, group), {})

    if params['user_password']:
        try:
            pw_check = open_url(
                '{0}/auth/test'.format(client.url),
                url_username=params['name'],
                url_password=params['user_password'],
                force_basic_auth=True,
            )
        except HTTPError as e:
            if e.code == 401:
                changed = True
                if not module.check_mode:
                    payload = {
                        'username': params['name'],
                        'password': params['user_password'],
                    }
                    client.put('{0}/password'.format(user_path), payload)
        except URLError:
            pass

    if changed:
        user = client.get(user_path)

    module.exit_json(changed=changed, user=user)


if __name__ == '__main__':
    main()
