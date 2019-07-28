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
module: sensu_go_rolebinding
author: "Paul Arthur (@flowerysong)"
short_description: Manages Sensu role bindings
description:
  - 'For more information, refer to the Sensu documentation: U(https://docs.sensu.io/sensu-go/latest/reference/rbac/)'
extends_documentation_fragment:
  - flowerysong.sensu_go.base
options:
  name:
    description:
      - The Sensu object's name.
    required: yes
  state:
    description:
      - Target state of the Sensu object.
    choices: [ 'present', 'absent' ]
    default: present
  cluster:
    description:
      - Operate against cluster role bindings instead of namespaced bindings
    type: bool
    default: false
  cluster_role:
    description:
      - Use a cluster role in a namespaced binding (has no effect when cluster is true)
  role:
    description:
      - Role name
  users:
    description:
      - List of users to bind to the role
  groups:
    description:
      - List of groups to bind to the role
'''

EXAMPLES = '''
- name: Give admins global access
  sensu_go_rolebinding:
    name: admins-admin
    cluster: true
    role: cluster-admin
    groups:
      - admins

- name: Give nagios admins namespaced access
  sensu_go_rolebinding:
    name: nagios-admins-fence
    namespace: nagios
    cluster_role: true
    role: admin
    groups:
      - nagios-admins

- name: A special role for a special boy
  sensu_go_rolebinding:
    name: nagios-ex-admins-fence
    namespace: nagios
    role: read-entities
    users:
      - brywilk
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.flowerysong.sensu_go.plugins.module_utils.base import AnsibleSensuClient, SensuObject, sensu_argument_spec


class SensuRoleBinding(SensuObject):
    def __init__(self, module):
        self.module = module
        self.client = AnsibleSensuClient(module)
        self.params = module.params
        self.payload = {
            'metadata': {
                'name': self.params['name'],
            },
        }

        if module.params['cluster']:
            self.client.namespace = None
            self.path = '/clusterrolebindings/{0}'.format(self.params['name'])
        else:
            self.path = '/rolebindings/{0}'.format(self.params['name'])
            self.payload['metadata']['namespace'] = self.params['namespace']

        self.payload['role_ref'] = {
            'type': 'Role',
            'name': self.params['role'],
        }

        if module.params['cluster'] or module.params['cluster_role']:
            self.payload['role_ref']['type'] = 'ClusterRole'

        subjects = []
        for u in self.params['users']:
            subjects.append({
                'name': u,
                'type': 'User',
            })

        for g in self.params['groups']:
            subjects.append({
                'name': g,
                'type': 'Group',
            })

        self.payload['subjects'] = subjects


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
        cluster_role=dict(
            type='bool',
            default=False,
        ),
        role=dict(),
        users=dict(
            type='list',
            elements='str',
            default=[]
        ),
        groups=dict(
            type='list',
            elements='str',
            default=[]
        ),
    ))

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
        required_if=[('state', 'present', ['role'])],
    )

    rb = SensuRoleBinding(module)
    result = rb.reconcile()
    module.exit_json(changed=result['changed'], rolebinding=result['object'])


if __name__ == '__main__':
    main()
