#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Paul Arthur <paul.arthur@flowerysong.com>
# Copyright: (c) 2019, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'XLAB Steampunk'}

DOCUMENTATION = '''
module: user
author:
  - Paul Arthur (@flowerysong)
  - Aljaz Kosir (@aljazkosir)
  - Tadej Borovsak (@tadeboro)
short_description: Manages Sensu users
description:
  - For more information, refer to the Sensu documentation at
    U(https://docs.sensu.io/sensu-go/latest/reference/users/)
extends_documentation_fragment:
  - sensu.sensu_go.base
notes:
  - Parameter C(auth.namespace) is ignored in this module.
options:
  state:
    description:
      - Desired state of the user.
      - Users cannot actually be deleted, only deactivated.
    type: str
    choices: ['enabled', 'disabled']
    default: enabled
  name:
    description:
      - Username.
    type: str
    required: true
  password:
    description:
      - Password for the user.
    type: str
  groups:
    description:
      - List of groups user belongs to.
    type: list
'''

EXAMPLES = '''
- name: Create a user
  user:
    auth:
      url: http://localhost:8080
    name: awesome_username
    password: hidden_password?
    groups:
      - dev
      - prod
'''

RETURN = '''
object:
    description: object representing Sensu user
    returned: success
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    arguments, errors, utils,
)


def sync(remote_object, state, client, path, payload, check_mode):
    if state == 'disabled' and remote_object is not None:
        if not check_mode:
            utils.delete(client, path)
        return True, utils.get(client, path)

    if utils.do_differ(remote_object, payload):
        if check_mode:
            return True, payload
        utils.put(client, path, payload)
        return True, utils.get(client, path)

    return False, remote_object


def main():
    required_if = [
        ('state', 'enabled', ('password', ))
    ]
    module = AnsibleModule(
        required_if=required_if,
        supports_check_mode=True,
        argument_spec=dict(
            arguments.get_spec("auth", "name"),
            state=dict(
                default='enabled',
                choices=['enabled', 'disabled'],
            ),
            password=dict(
                no_log=True
            ),
            groups=dict(
                type='list',
            )
        ),
    )

    module.params['auth']['namespace'] = None
    client = arguments.get_sensu_client(module.params['auth'])
    path = '/users/{0}'.format(module.params['name'])
    state = module.params['state']

    remote_object = utils.get(client, path)
    if remote_object is None and state == 'disabled' and module.params['password'] is None:
        module.fail_json(msg='Cannot disable a non existent user')

    payload = arguments.get_spec_payload(module.params, 'password', 'groups')
    payload['username'] = module.params['name']
    payload['disabled'] = module.params['state'] == 'disabled'

    try:
        changed, user = sync(
            remote_object, state, client, path, payload, module.check_mode
        )
        module.exit_json(changed=changed, object=user)
    except errors.Error as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
