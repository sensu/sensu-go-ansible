#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Paul Arthur <paul.arthur@flowerysong.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'XLAB Steampunk'}

DOCUMENTATION = '''
module: namespace_info
author:
  - Paul Arthur (@flowerysong)
  - Aljaz Kosir (@aljazkosir)
  - Miha Plesko (@miha-plesko)
  - Tadej Borovsak (@tadeboro)
short_description: Lists Sensu namespaces
description:
  - For more information, refer to the Sensu documentation at
    U(https://docs.sensu.io/sensu-go/latest/reference/rbac/#namespaces)
extends_documentation_fragment:
  - sensu.sensu_go.base
notes:
  - Parameters C(auth.namespace) is ignored in this module.
'''

EXAMPLES = '''
- name: List Sensu namespaces
  namespace_info:
  register: result
'''

RETURN = '''
objects:
  description: list of Sensu namespaces
  returned: always
  type: list
'''

from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    arguments, errors, utils,
)


def main():
    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=dict(
            arguments.COMMON_ARGUMENTS,
        ),
    )
    module.params['auth']['namespace'] = None
    client = arguments.get_sensu_client(module.params['auth'])
    path = '/namespaces'

    try:
        namespaces = utils.get(client, path)
    except errors.Error as e:
        module.fail_json(msg=str(e))

    module.exit_json(changed=False, objects=namespaces)


if __name__ == '__main__':
    main()
