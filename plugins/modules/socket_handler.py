#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'XLAB Steampunk'}

DOCUMENTATION = '''
module: socket_handler
author:
  - Aljaz Kosir (@aljazkosir)
  - Miha Plesko (@miha-plesko)
  - Tadej Borovsak (@tadeboro)
short_description: Manages Sensu TCP/UDP handler
description:
  - For more information, refer to the Sensu documentation at
    U(https://docs.sensu.io/sensu-go/latest/reference/handlers/)
extends_documentation_fragment:
  - sensu.sensu_go.auth
  - sensu.sensu_go.name
  - sensu.sensu_go.state
  - sensu.sensu_go.labels
  - sensu.sensu_go.annotations
options:
  type:
    description:
      - The handler type.
    choices:
      - tcp
      - udp
    type: str
    required: true
  filters:
    description:
      - List of filters to use when determining whether to pass the check result to this handler.
    type: list
  mutator:
    description:
      - Mutator to call for transforming the check result before passing it to this handler.
    type: str
  timeout:
    description:
      - Timeout for handler execution
    type: int
  host:
    description:
      - The socket host address (IP or hostname) to connect to.
    required: true
    type: str
  port:
    description:
      - The socket port to connect to.
    type: int
    required: true
'''

EXAMPLES = '''
- name: TCP handler
  socket_handler:
    name: tcp_handler
    type: tcp
    host: 10.0.1.99
    port: 4444

- name: UDP handler
  socket_handler:
    name: udp_handler
    type: udp
    host: 10.0.1.99
    port: 4444
'''

RETURN = '''
object:
    description: object representing Sensu socket handler
    returned: success
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    arguments, errors, utils,
)


def main():
    required_if = [
        ('state', 'present', ['type', 'host', 'port'])
    ]
    module = AnsibleModule(
        supports_check_mode=True,
        required_if=required_if,
        argument_spec=dict(
            arguments.get_spec(
                "auth", "name", "state", "labels", "annotations",
            ),
            type=dict(choices=['tcp', 'udp']),
            filters=dict(
                type='list',
            ),
            mutator=dict(),
            timeout=dict(
                type='int'
            ),
            host=dict(),
            port=dict(
                type='int'
            )
        ),
    )

    client = arguments.get_sensu_client(module.params['auth'])
    path = utils.build_url_path('handlers', module.params['name'])
    payload = arguments.get_mutation_payload(
        module.params, 'type', 'filters', 'mutator', 'timeout'
    )
    payload['socket'] = dict(host=module.params['host'], port=module.params['port'])

    try:
        changed, handler = utils.sync(
            module.params['state'], client, path, payload, module.check_mode,
        )
        module.exit_json(changed=changed, object=handler)
    except errors.Error as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
