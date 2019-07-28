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
module: sensu_go_hook
author: "Paul Arthur (@flowerysong)"
short_description: Manages Sensu hooks
description:
  - 'For more information, refer to the Sensu documentation: U(https://docs.sensu.io/sensu-go/latest/reference/hooks/)'
extends_documentation_fragment:
  - flowerysong.sensu_go.base
  - flowerysong.sensu_go.object
options:
  command:
    description:
      - Command to run when the hook is triggered.
    required: true
  timeout:
    description:
      - Hook execution timeout, in seconds.
    type: int
    default: 60
  stdin:
    description:
      - Controls whether Sensu writes serialized JSON data to the process's stdin.
    type: bool
    default: false
'''

EXAMPLES = '''
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.flowerysong.sensu_go.plugins.module_utils.base import SensuObject


class SensuHook(SensuObject):
    def __init__(self, module):
        super(SensuHook, self).__init__(module)

        self.path = '/hooks/{0}'.format(self.params['name'])
        for key in ('command', 'timeout', 'stdin'):
            self.payload[key] = self.params[key]


def main():
    argspec = SensuHook.argument_spec()
    argspec.update(dict(
        command=dict(),
        timeout=dict(
            type='int',
            default=60,
        ),
        stdin=dict(
            type='bool',
            default=False,
        ),
    ))

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
        required_if=[('state', 'present', ['command'])],
    )

    hook = SensuHook(module)
    result = hook.reconcile()
    module.exit_json(changed=result['changed'], hook=result['object'])


if __name__ == '__main__':
    main()
