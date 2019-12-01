#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Paul Arthur <paul.arthur@flowerysong.com>
# Copyright: (c) 2019, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["stableinterface"],
    "supported_by": "certified",
}

DOCUMENTATION = '''
module: role_binding
author:
 - Paul Arthur (@flowerysong)
 - Manca Bizjak (@mancabizjak)
 - Aljaz Kosir (@aljazkosir)
 - Tadej Borovsak (@tadeboro)
short_description: Manage Sensu role bindings
description:
  - Create, update or delete Sensu role binding.
  - For more information, refer to the Sensu documentation at
    U(https://docs.sensu.io/sensu-go/latest/reference/rbac/#role-bindings-and-cluster-role-bindings).
version_added: "1.0"
extends_documentation_fragment:
  - sensu.sensu_go.auth
  - sensu.sensu_go.name
  - sensu.sensu_go.state
options:
  role:
    description:
      - Name of the role
      - This parameter is mutually exclusive with C(cluster_role).
    type: str
  cluster_role:
    description:
      - Name of the cluster role. Note that the resulting role
        binding grants the cluster role to the provided users and
        groups in the context of C(auth.namespace) only.
      - This parameter is mutually exclusive with C(role).
    type: str
  users:
    description:
      - List of users to bind to the role or cluster role
      - Note that at least one of C(users) and C(groups) must be
        specified when creating a role binding.
    type: list
  groups:
    description:
      - List of groups to bind to the role or cluster role
      - Note that at least one of C(users) and C(groups) must be
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

- name: Create a role binding for admins
  role_binding:
    name: org-admins
    cluster_role: admin
    groups:
      - team1-admins
      - team2-admins
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


def infer_role(params):
    if params["role"]:
        return "Role", params["role"]
    return "ClusterRole", params["cluster_role"]


def build_api_payload(params):
    payload = arguments.get_mutation_payload(params)
    payload["subjects"] = role_utils.build_subjects(params["groups"], params["users"])
    payload["role_ref"] = role_utils.type_name_dict(*infer_role(params))

    return payload


def main():
    required_if = [
        ("state", "present", ["role", "cluster_role"], True)  # True means any of role, cluster_role
    ]
    mutually_exclusive = [
        ["role", "cluster_role"]
    ]
    module = AnsibleModule(
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
        argument_spec=dict(
            arguments.get_spec("auth", "name", "state"),
            role=dict(),
            cluster_role=dict(),
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
    path = utils.build_url_path("rolebindings", module.params["name"])
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
