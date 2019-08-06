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
module: sensu_go_rolebinding_info
author: "Paul Arthur (@flowerysong)"
short_description: Lists Sensu role bindings
description:
  - 'For more information, refer to the Sensu documentation: U(https://docs.sensu.io/sensu-go/latest/reference/rbac/)'
version_added: 0.1.0
extends_documentation_fragment:
  - sensu.sensu_go.base
  - sensu.sensu_go.info
options:
  cluster:
    description:
      - Operate against cluster role bindings instead of namespaced bindings
    type: bool
    default: false
'''

EXAMPLES = '''
- name: List Sensu role bindings
  sensu_go_rolebinding_info:
  register: result
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.sensu.sensu_go.plugins.module_utils.base import sensu_argument_spec, AnsibleSensuClient


def main():
    argspec = sensu_argument_spec()
    argspec.update(
        dict(
            name=dict(),
            cluster=dict(type='bool', default=False),
        )
    )

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
    )

    endpoint = '/rolebindings'
    client = AnsibleSensuClient(module)
    if module.params['cluster']:
        client.namespace = None
        endpoint = '/clusterrolebindings'

    if module.params['name']:
        result = [client.get('{0}/{1}'.format(endpoint, module.params['name']))]
    else:
        result = client.get(endpoint)

    module.exit_json(changed=False, rolebindings=result)


if __name__ == '__main__':
    main()
