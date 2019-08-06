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
module: sensu_go_role
author: "Paul Arthur (@flowerysong)"
short_description: Manages Sensu roles
description:
  - 'For more information, refer to the Sensu documentation: U(https://docs.sensu.io/sensu-go/latest/reference/rbac/)'
version_added: 0.1.0
extends_documentation_fragment:
  - sensu.sensu_go.base
options:
  name:
    description:
      - The Sensu object's name.
    type: str
    required: yes
  state:
    description:
      - Target state of the Sensu object.
    type: str
    choices: [ 'present', 'absent' ]
    default: present
  cluster:
    description:
      - Operate against cluster roles instead of namespaced roles
    type: bool
    default: false
  rules:
    description:
      - Role rules
    type: list
'''

EXAMPLES = '''
- name: Create new role
  sensu_go_role:
    name: readonly
    namespace: default
    rules:
      - verbs:
          - get
          - list
        resources: '*'

- name: Create new cluster role
  sensu_go_role:
    name: asset-manager
    cluster: true
    rules:
      - verbs: '*'
        resources: assets
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.sensu.sensu_go.plugins.module_utils.base import AnsibleSensuClient, SensuObject, sensu_argument_spec


class SensuRole(SensuObject):
    def __init__(self, module):
        self.module = module
        self.client = AnsibleSensuClient(module)
        self.params = module.params
        self.payload = {
            'metadata': {
                'name': self.params['name'],
            },
        }
        cluster = module.params['cluster']

        if cluster:
            self.client.namespace = None
            self.path = '/clusterroles/{0}'.format(self.params['name'])
        else:
            self.path = '/roles/{0}'.format(self.params['name'])
            self.payload['metadata']['namespace'] = module.params['namespace']

        for r in self.params['rules']:
            for key in ('resources', 'verbs', 'resource_names'):
                if key in r:
                    if not isinstance(r[key], list):
                        r[key] = [r[key]]
                else:
                    r[key] = None

        self.payload['rules'] = self.params['rules']


def main():
    argspec = sensu_argument_spec()
    argspec.update(dict(
        name=dict(required=True),
        state=dict(
            default='present',
            choices=['present', 'absent'],
        ),
        cluster=dict(
            type='bool',
            default=False,
        ),
        rules=dict(
            type='list',
            elements='dict',
            default=[],
        ),
    ))

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
        required_if=[('state', 'present', ['rules'])],
    )

    role = SensuRole(module)
    result = role.reconcile()
    module.exit_json(changed=result['changed'], role=result['object'])


if __name__ == '__main__':
    main()
