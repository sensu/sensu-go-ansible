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
module: cluster_role
author:
 - Paul Arthur (@flowerysong)
 - Manca Bizjak (@mancabizjak)
 - Aljaz Kosir (@aljazkosir)
 - Tadej Borovsak (@tadeboro)
short_description: Manages Sensu cluster roles
description:
  - For more information, refer to the Sensu documentation at
    U(https://docs.sensu.io/sensu-go/latest/reference/rbac/)
extends_documentation_fragment:
  - sensu.sensu_go.auth
  - sensu.sensu_go.name
  - sensu.sensu_go.state
notes:
  - Parameter C(auth.namespace) is ignored in this module.
options:
  rules:
    description:
      - Rules that the cluster role applies.
    type: list
    suboptions:
      verbs:
        description:
          - Permissions to be applied by the rule.
        type: list
        required: yes
        choices: [get, list, create, update, delete]
      resources:
        description:
          - Types of resources the rule has permission to access.
        type: list
        required: yes
      resource_names:
        description:
          - Names of specific resources the rule has permission to access.
          - Note that for the 'create' verb, this argument will not be
            taken into account when enforcing RBAC, even if it is provided.
        type: list
'''

EXAMPLES = '''
- name: Create a cluster role
  cluster_role:
    name: readonly
    rules:
      - verbs:
          - get
          - list
        resources:
          - checks
          - entities
'''

RETURN = '''
object:
    description: object representing Sensu cluster role
    returned: success
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    arguments, errors, utils, role_utils
)


def validate_module_params(module):
    params = module.params
    if params['state'] == 'present':
        if not params['rules']:
            module.fail_json(
                msg='state is present but all of the following are missing: rules'
            )


def main():
    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=dict(
            arguments.get_spec("auth", "name", "state"),
            rules=dict(
                type="list",
                elements="dict",
                options=dict(
                    verbs=dict(
                        required=True,
                        type="list",
                        choices=["get", "list", "create", "update", "delete"],
                    ),
                    resources=dict(
                        required=True,
                        type="list",
                    ),
                    resource_names=dict(
                        type="list",
                    ),
                )
            )
        )
    )

    validate_module_params(module)
    module.params['auth']['namespace'] = None  # Making sure we are not fallbacking to default
    client = arguments.get_sensu_client(module.params["auth"])
    path = "/clusterroles/{0}".format(module.params["name"])
    payload = arguments.get_mutation_payload(
        module.params, "rules"
    )

    try:
        changed, cluster_role = utils.sync(
            module.params['state'], client, path,
            payload, module.check_mode, role_utils.do_roles_differ
        )
        module.exit_json(changed=changed, object=cluster_role)
    except errors.Error as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
