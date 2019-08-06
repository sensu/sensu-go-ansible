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
module: sensu_go_tessen
author: "Paul Arthur (@flowerysong)"
short_description: Manages Sensu's phone-home configuration
description:
  - Tessen cannot be disabled in licensed instances.
  - 'For more information, refer to the Sensu documentation: U(https://docs.sensu.io/sensu-go/latest/reference/tessen/)'
version_added: 0.1.0
extends_documentation_fragment:
  - sensu.sensu_go.base
options:
  enabled:
    description:
      - Enable or disable phoning home.
    type: bool
    default: false
'''

EXAMPLES = '''
- name: Disable Tessen
  sensu_go_tessen:
    state: disabled
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
            enabled=dict(
                type='bool',
                default=False,
            ),
        )
    )

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
    )

    client = AnsibleSensuClient(module)
    client.namespace = None

    result = client.get('/tessen')

    changed = False
    if result['opt_out'] == module.params['enabled']:
        changed = True
        if not module.check_mode:
            payload = {
                'opt_out': not module.params['enabled'],
            }
            client.put('/tessen', payload)

    module.exit_json(changed=changed)


if __name__ == '__main__':
    main()
