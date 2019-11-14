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
module: role_binding
author:
 - Paul Arthur (@flowerysong)
 - Manca Bizjak (@mancabizjak)
 - Aljaz Kosir (@aljazkosir)
 - Tadej Borovsak (@tadeboro)
short_description: Manages Sensu role bindings
description:
  - For more information, refer to the Sensu documentation at
    U(https://docs.sensu.io/sensu-go/latest/reference/rbac/)
extends_documentation_fragment:
  - sensu.sensu_go.auth
  - sensu.sensu_go.name
  - sensu.sensu_go.state
options:
  role:
    description:
      - Name of the role
    type: str
  users:
    description:
      - List of users to bind to the role
      - Note that at least one of 'users' and 'groups' must be
        specified when creating a role binding.
    type: list
  groups:
    description:
      - List of groups to bind to the role
      - Note that at least one of 'users' and 'groups' must be
        specified when creating a role binding.
    type: list
'''

EXAMPLES = '''
- name: Create a role binding
  role_binding:
    name: dev_and_testing
    role: testers_permissive
    groups:
        - testers
        - dev
        - ops
    users:
      - alice
'''

RETURN = '''
object:
    description: object representing Sensu role binding
    returned: success
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    arguments, errors, utils, role_utils
)


def build_api_payload(params):
    payload = arguments.get_mutation_payload(params)
    payload["subjects"] = role_utils.build_subjects(params["groups"], params["users"])
    payload["role_ref"] = role_utils.type_name_dict("Role", params["role"])

    return payload


def main():
    required_if = [
        ("state", "present", ["role"])
    ]
    module = AnsibleModule(
        required_if=required_if,
        supports_check_mode=True,
        argument_spec=dict(
            arguments.get_spec("auth", "name", "state"),
            role=dict(),
            users=dict(
                type="list",
            ),
            groups=dict(
                type="list",
            ),
        )
    )

    msg = role_utils.validate_binding_module_params(module.params)
    if msg:
        module.fail_json(msg=msg)

    client = arguments.get_sensu_client(module.params["auth"])
    path = "/rolebindings/{0}".format(module.params["name"])
    payload = build_api_payload(module.params)

    try:
        changed, role_binding = utils.sync(
            module.params["state"], client, path, payload, module.check_mode, role_utils.do_role_bindings_differ
        )
        module.exit_json(changed=changed, object=role_binding)
    except errors.Error as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
