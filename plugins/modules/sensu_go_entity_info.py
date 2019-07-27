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
module: sensu_go_entity_info
author: "Paul Arthur (@flowerysong)"
short_description: Lists Sensu entities
description:
  - 'For more information, refer to the Sensu documentation: U(https://docs.sensu.io/sensu-go/latest/reference/entities/)'
extends_documentation_fragment:
  - flowerysong.sensu_go.base
  - flowerysong.sensu_go.info
'''

EXAMPLES = '''
# List all entities
- name: List Sensu entities
  sensu_go_entity_info:
  register: result
'''

RETURN = '''
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
        result = [client.get('/entities/{0}'.format(module.params['name']))]
    else:
        result = client.get('/entities')

    module.exit_json(changed=False, entities=result)


if __name__ == '__main__':
    main()
