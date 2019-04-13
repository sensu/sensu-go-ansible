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
        update_password=dict(
            default='on_create',
            choices=['always', 'on_create'],
        )
    ))

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
    )

    client = AnsibleSensuClient(module)
    client.namespace = None

    params = module.params
    user_path = '/users/{0}'.format(params['name'])

    payload = {
        'username': params['name'],
        'groups': params['groups'],
        'disabled': params['state'] == 'absent',
    }

    old = client.get(user_path)
    if params['state'] == 'absent':
        if not old or old['disabled']:
            module.exit_json(changed=False, user={})
        if not module.check_mode:
            client.delete(user_path)
        module.exit_json(changed=True, user=old)

    if old and not params['purge_groups']:
        payload['groups'] = list(set( payload['groups'] + old['groups']))

    if not old or (params['user_password'] and params['update_password'] == 'always'):
        payload['password'] = params['user_password']

    changed = False
    for key in payload:
        if payload[key] != old.get(key):
            changed = True

    if changed and not module.check_mode:
        old = client.put(user_path, payload)

    module.exit_json(changed=changed, user=old)


if __name__ == '__main__':
    main()
