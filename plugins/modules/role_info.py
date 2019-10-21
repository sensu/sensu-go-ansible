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
module: role_info
author:
  - Paul Arthur (@flowerysong)
  - Manca Bizjak (@mancabizjak)
  - Aljaz Kosir (@aljazkosir)
  - Tadej Borovsak (@tadeboro)
short_description: Lists Sensu roles
description:
  - For more information, refer to the Sensu documentation at
    U(https://docs.sensu.io/sensu-go/latest/reference/rbac/)
version_added: 0.1.0
extends_documentation_fragment:
  - sensu.sensu_go.base
  - sensu.sensu_go.info
'''

EXAMPLES = '''
- name: List all Sensu roles
  role_info:
  register: result
'''

RETURN = '''
roles:
  description: list of Sensu roles
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

    client = arguments.get_sensu_client(module.params["auth"])
    if module.params["name"]:
        path = "/roles/{0}".format(module.params["name"])
    else:
        path = "/roles"

    try:
        roles = utils.get(client, path)
    except errors.Error as e:
        module.fail_json(msg=str(e))

    if module.params["name"]:
        roles = [roles]
    module.exit_json(changed=False, objects=roles)


if __name__ == '__main__':
    main()
