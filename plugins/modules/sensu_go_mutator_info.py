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
module: sensu_go_mutator_info
author: "Paul Arthur (@flowerysong)"
short_description: Lists Sensu mutators
description:
  - 'For more information, refer to the Sensu documentation: U(https://docs.sensu.io/sensu-go/latest/reference/mutators/)'
version_added: 0.1.0
extends_documentation_fragment:
  - flowerysong.sensu_go.base
  - flowerysong.sensu_go.info
'''

EXAMPLES = '''
- name: List Sensu mutators
  sensu_go_mutator_info:
  register: result
'''

RETURN = '''
mutators:
  description: list of Sensu mutators
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

    if module.params['name']:
        result = [client.get('/mutators/{0}'.format(module.params['name']))]
    else:
        result = client.get('/mutators')

    module.exit_json(changed=False, mutators=result)


if __name__ == '__main__':
    main()
