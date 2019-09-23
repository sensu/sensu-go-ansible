#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Paul Arthur <paul.arthur@flowerysong.com>
# Copyright: (c) 2019, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'XLAB Steampunk'}

DOCUMENTATION = '''
module: mutator
author:
  - Paul Arthur (@flowerysong)
  - Aljaz Kosir (@aljazkosir)
  - Miha Plesko (@miha-plesko)
  - Tadej Borovsak (@tadeboro)
short_description: Manages Sensu mutators
description:
  - For more information, refer to the Sensu documentation at
    U(https://docs.sensu.io/sensu-go/latest/reference/mutators/)
extends_documentation_fragment:
  - sensu.sensu_go.base
  - sensu.sensu_go.object
options:
  command:
    description:
      - The mutator command to be executed by the Sensu backend.
    type: str
  timeout:
    description:
      - The mutator execution duration timeout in seconds (hard stop).
    type: int
  env_vars:
    description:
      - A mapping of environment variable names and values to use with command execution.
    type: dict
  runtime_assets:
    description:
      - List of runtime assets to required to run the mutator C(command)
    type: list
'''

EXAMPLES = '''
- name: Create a mutator
  mutator:
    name: mutator
    command: sensu-influxdb-mutator
    timeout: 30
    env_vars:
      INFLUXDB_ADDR: http://influxdb.default.svc.cluster.local:8086
      INFLUXDB_USER: sensu
    runtime_assets:
      - sensu-influxdb-mutator
'''

RETURN = '''
object:
    description: object representing Sensu mutator
    returned: success
    type: dict
'''


from ansible.module_utils.basic import AnsibleModule

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    arguments, errors, utils,
)


def main():
    required_if = [
        ('state', 'present', ['command'])
    ]
    module = AnsibleModule(
        required_if=required_if,
        supports_check_mode=True,
        argument_spec=dict(
            arguments.MUTATION_ARGUMENTS,
            command=dict(),
            timeout=dict(
                type='int',
            ),
            env_vars=dict(
                type='dict'
            ),
            runtime_assets=dict(
                type='list'
            ),
        ),
    )

    client = arguments.get_sensu_client(module.params['auth'])
    path = '/mutators/{0}'.format(module.params['name'])
    payload = arguments.get_mutation_payload(
        module.params, 'command', 'timeout', 'runtime_assets'
    )
    if module.params['env_vars']:
        payload['env_vars'] = utils.dict_to_key_value_strings(module.params['env_vars'])
    try:
        changed, mutator = utils.sync(
            module.params['state'], client, path, payload, module.check_mode,
        )
        module.exit_json(changed=changed, object=mutator)
    except errors.Error as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
