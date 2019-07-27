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
module: sensu_go_handler
author: "Paul Arthur (@flowerysong)"
short_description: Manages Sensu handlers
description:
  - 'For more information, refer to the Sensu documentation: U(https://docs.sensu.io/sensu-go/latest/reference/handlers/)'
extends_documentation_fragment:
  - flowerysong.sensu_go.base
  - flowerysong.sensu_go.object
options:
  type:
    description:
      - Handler type.
    choices: [ 'pipe', 'tcp', 'udp', 'set' ]
    default: pipe
  command:
    description:
      - Command to C(pipe) the check result data into.
  filters:
    description:
      - List of filters to use when determining whether to pass the check result to this handler.
    type: list
  mutator:
    description:
      - Mutator to call for transforming the check result before passing it to this handler.
  timeout:
    description:
      - Timeout for handler execution
    type: int
    default: 60
  env_vars:
    description:
      - A mapping of environment variable names and values to use with command execution.
    type: dict
  socket_host:
    description:
      - Hostname to connect to for C(tcp) or C(udp)
  socket_port:
    description:
      - Port to connect to for C(tcp) or C(udp)
  handlers:
    description:
      - List of handlers that comprise this C(set)
    type: list
  runtime_assets:
    description:
      - List of runtime assets to required to run the handler C(command)
'''

EXAMPLES = '''
sensu_go_handler:
  name: influx-db
  type: pipe
  command: sensu-influxdb-handler -d sensu
  env_vars:
    INFLUXDB_ADDR: http://influxdb.default.svc.cluster.local:8086
    INFLUXDB_USER: sensu
    INFLUXDB_PASS: password
  runtime_assets:
    - sensu-influxdb-handler
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.validation import check_missing_parameters
from ansible.module_utils._text import to_native

from ansible_collections.flowerysong.sensu_go.plugins.module_utils.base import SensuObject


class SensuHandler(SensuObject):
    def __init__(self, module):
        super(SensuHandler, self).__init__(module)

        self.path = '/handlers/{0}'.format(self.params['name'])
        for key in ('type', 'filters', 'mutator', 'timeout', 'command', 'handlers', 'runtime_assets'):
            if self.params[key] is not None:
                self.payload[key] = self.params[key]

        self.param_dict_to_payload_kv_list('env_vars')

        if self.params['type'] in ('tcp', 'udp'):
            self.payload['socket'] = {
                'host': self.params['socket_host'],
                'port': self.params['socket_port'],
            }


def main():
    argspec = SensuHandler.argument_spec()
    argspec.update(dict(
        type=dict(
            default='pipe',
            choices=['pipe', 'tcp', 'udp', 'set'],
        ),
        filters=dict(
            type='list',
        ),
        mutator=dict(),
        timeout=dict(
            type='int',
            default=60,
        ),
        command=dict(),
        env_vars=dict(
            type='dict',
        ),
        socket_host=dict(),
        socket_port=dict(),
        handlers=dict(
            type='list',
        ),
        runtime_assets=dict(
            type='list',
        ),
    ))

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
    )

    # We only care about this if we're creating the handler, so we can't
    # use `required_if`
    if module.params['state'] == 'present':
        requirements = [
            ('pipe', ['command']),
            ('tcp', ['socket_host', 'socket_port']),
            ('udp', ['socket_host', 'socket_port']),
            ('set', ['handlers']),
        ]
        for req in requirements:
            if module.params['type'] == req[0]:
                try:
                    check_missing_parameters(module.params, req[1])
                except TypeError as e:
                    msg = to_native(e)
                    module.fail_json(msg=msg)

    handler = SensuHandler(module)
    result = handler.reconcile()
    module.exit_json(changed=result['changed'], handler=result['object'])


if __name__ == '__main__':
    main()
