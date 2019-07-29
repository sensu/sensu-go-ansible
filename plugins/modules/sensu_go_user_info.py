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
module: sensu_go_user_info
author: "Paul Arthur (@flowerysong)"
short_description: Lists Sensu users
description:
  - 'For more information, refer to the Sensu documentation: U(https://docs.sensu.io/sensu-go/latest/reference/users/)'
version_added: 0.1.0
extends_documentation_fragment:
  - flowerysong.sensu_go.base
  - flowerysong.sensu_go.info
'''

EXAMPLES = '''
- name: List Sensu users
  sensu_go_user_info:
  register: result
'''

RETURN = '''
users:
  description: list of Sensu users
  returned: always
  type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.flowerysong.sensu_go.plugins.module_utils.base import sensu_argument_spec, AnsibleSensuClient


def main():
    argspec = sensu_argument_spec()
    argspec.update(
        dict(
            name=dict(),
        )
    )

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
    )

    client = AnsibleSensuClient(module)
    client.namespace = None

    if module.params['name']:
        result = [client.get('/users/{0}'.format(module.params['name']))]
    else:
        result = client.get('/users')

    module.exit_json(changed=False, users=result)


if __name__ == '__main__':
    main()
