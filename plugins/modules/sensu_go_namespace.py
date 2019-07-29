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
module: sensu_go_namespace
author: "Paul Arthur (@flowerysong)"
short_description: Manages Sensu namespaces
description:
  - 'For more information, refer to the Sensu documentation: U(https://docs.sensu.io/sensu-go/latest/reference/rbac/)'
version_added: 0.1.0
extends_documentation_fragment:
  - flowerysong.sensu_go.base
options:
  namespace:
    description:
      - Name of the namespace
    aliases:
      - name
    type: str
    default: ~
    required: true
  state:
    description:
      - Desired state of the namespace.
    type: str
    choices: ['present', 'absent']
    default: present
'''

EXAMPLES = '''
# Create a new namespace
- sensu_go_namespace:
    name: production
    state: present

# Delete a namespace
- sensu_go_namespace:
    name: staging
    state: absent
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.flowerysong.sensu_go.plugins.module_utils.base import sensu_argument_spec, AnsibleSensuClient


def main():
    argspec = sensu_argument_spec()
    argspec.update(
        dict(
            state=dict(
                choices=['present', 'absent'],
                default='present',
            ),
            namespace=dict(
                aliases=['name'],
                required=True,
            ),
        )
    )

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
    )

    client = AnsibleSensuClient(module)
    client.namespace = None

    result = client.get('/namespaces')

    for ns in result:
        if ns['name'] == module.params['name']:
            if module.params['state'] == 'present':
                module.exit_json(changed=False)
            if not module.check_mode:
                client.delete('/namespaces/{0}'.format(module.params['name']))
            module.exit_json(changed=True)

    if module.params['state'] == 'absent':
        module.exit_json(changed=False)

    if not module.check_mode:
        payload = {'name': module.params['name']}
        client.put('/namespaces/{0}'.format(module.params['name']), payload)

    module.exit_json(changed=True)


if __name__ == '__main__':
    main()
