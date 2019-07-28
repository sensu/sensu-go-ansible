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
module: sensu_go_mutator
author: "Paul Arthur (@flowerysong)"
short_description: Manages Sensu mutators
description:
  - 'For more information, refer to the Sensu documentation: U(https://docs.sensu.io/sensu-go/latest/reference/mutators/)'
extends_documentation_fragment:
  - flowerysong.sensu_go.base
  - flowerysong.sensu_go.object
options:
  command:
    description:
      - Command to C(pipe) the check result data into.
  timeout:
    description:
      - Timeout for mutator execution
    type: int
    default: 60
  env_vars:
    description:
      - A mapping of environment variable names and values to use with command execution.
    type: dict
  runtime_assets:
    description:
      - List of runtime assets to required to run the mutator C(command)
'''

EXAMPLES = '''
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.flowerysong.sensu_go.plugins.module_utils.base import SensuObject


class SensuMutator(SensuObject):
    def __init__(self, module):
        super(SensuMutator, self).__init__(module)

        self.path = '/mutators/{0}'.format(self.params['name'])
        for key in ('timeout', 'command', 'runtime_assets'):
            self.payload[key] = self.params[key]

        self.param_dict_to_payload_kv_list('env_vars')


def main():
    argspec = SensuMutator.argument_spec()
    argspec.update(dict(
        timeout=dict(
            type='int',
            default=60,
        ),
        command=dict(),
        env_vars=dict(
            type='dict',
            default={},
        ),
        runtime_assets=dict(
            type='list',
            default=[],
        ),
    ))

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
        required_if=[('state', 'present', ['command'])],
    )

    mutator = SensuMutator(module)
    result = mutator.reconcile()
    module.exit_json(changed=result['changed'], mutator=result['object'])


if __name__ == '__main__':
    main()
