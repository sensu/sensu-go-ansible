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
module: cluster_role_info
author:
  - Paul Arthur (@flowerysong)
  - Manca Bizjak (@mancabizjak)
  - Aljaz Kosir (@aljazkosir)
  - Tadej Borovsak (@tadeboro)
short_description: List Sensu cluster roles
description:
  - Retrieve information about Sensu roles.
  - For more information, refer to the Sensu documentation at
    U(https://docs.sensu.io/sensu-go/latest/reference/rbac/#roles-and-cluster-roles).
version_added: "1.0"
notes:
  - Parameter C(auth.namespace) is ignored in this module.
extends_documentation_fragment:
  - sensu.sensu_go.auth
  - sensu.sensu_go.info
'''

EXAMPLES = '''
- name: List all Sensu cluster roles
  role_info:
  register: result
'''

RETURN = '''
roles:
  description: list of Sensu cluster roles
  returned: always
  type: list
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    arguments, errors, utils,
)


def main():
    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=dict(
            arguments.get_spec("auth"),
            name=dict()
        ),
    )

    module.params['auth']['namespace'] = None  # Making sure we are not fallbacking to default
    client = arguments.get_sensu_client(module.params["auth"])
    path = utils.build_url_path("clusterroles", module.params["name"])

    try:
        cluster_roles = utils.get(client, path)
    except errors.Error as e:
        module.fail_json(msg=str(e))

    if module.params["name"]:
        cluster_roles = [cluster_roles]
    module.exit_json(changed=False, objects=cluster_roles)


if __name__ == '__main__':
    main()
