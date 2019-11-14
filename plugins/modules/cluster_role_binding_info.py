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
module: cluster_role_binding_info
author:
  - Paul Arthur (@flowerysong)
  - Manca Bizjak (@mancabizjak)
  - Aljaz Kosir (@aljazkosir)
  - Tadej Borovsak (@tadeboro)
short_description: Lists Sensu cluster role bindings
description:
  - For more information, refer to the Sensu documentation at
    U(https://docs.sensu.io/sensu-go/latest/reference/rbac/)
notes:
  - Parameter C(auth.namespace) is ignored in this module.
extends_documentation_fragment:
  - sensu.sensu_go.base
  - sensu.sensu_go.info
'''

EXAMPLES = '''
- name: List all Sensu cluster role bindings
  cluster_role_binding_info:
  register: result
'''

RETURN = '''
cluster_role_bindings:
  description: list of Sensu cluster role bindings
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
        )
    )

    module.params['auth']['namespace'] = None  # Making sure we are not fallbacking to default
    client = arguments.get_sensu_client(module.params["auth"])
    if module.params["name"]:
        path = "/clusterrolebindings/{0}".format(module.params["name"])
    else:
        path = "/clusterrolebindings"

    try:
        cluster_role_bindings = utils.get(client, path)
    except errors.Error as e:
        module.fail_json(msg=str(e))

    if module.params["name"]:
        cluster_role_bindings = [cluster_role_bindings]
    module.exit_json(changed=False, objects=cluster_role_bindings)


if __name__ == '__main__':
    main()
