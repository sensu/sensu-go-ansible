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
module: sensu_go_namespace_info
author: "Paul Arthur (@flowerysong)"
short_description: Lists Sensu namespaces
description:
  - 'For more information, refer to the Sensu documentation: U(https://docs.sensu.io/sensu-go/latest/reference/rbac/)'
version_added: 0.1.0
extends_documentation_fragment:
  - sensu.sensu_go.base
'''

EXAMPLES = '''
- name: List Sensu namespaces
  sensu_go_namespace_info:
  register: result
'''

RETURN = '''
namespaces:
  description: list of Sensu namespaces
  returned: always
  type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.sensu.sensu_go.plugins.module_utils.base import sensu_argument_spec, AnsibleSensuClient


def main():
    argspec = sensu_argument_spec()

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
    )

    client = AnsibleSensuClient(module)
    client.namespace = None

    result = client.get('/namespaces')
    result = [x['name'] for x in result]

    module.exit_json(changed=False, namespaces=result)


if __name__ == '__main__':
    main()
