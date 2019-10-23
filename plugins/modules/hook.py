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
module: hook
author:
  - Paul Arthur (@flowerysong)
  - Aljaz Kosir (@aljazkosir)
  - Miha Plesko (@miha-plesko)
  - Tadej Borovsak (@tadeboro)
short_description: Manages Sensu hooks
description:
  - For more information, refer to the Sensu documentation at
    U(https://docs.sensu.io/sensu-go/latest/reference/hooks/)
extends_documentation_fragment:
  - sensu.sensu_go.base
  - sensu.sensu_go.object
options:
  command:
    description:
      - Command to run when the hook is triggered.
    type: str
  timeout:
    description:
      - The hook execution duration timeout in seconds (hard stop).
    type: int
  stdin:
    description:
      - Controls whether Sensu writes serialized JSON data to the process's stdin.
    type: bool
  runtime_assets:
    description:
      - List of runtime assets required to run the check
    type: list
'''

EXAMPLES = '''
- name: Rudimentary auto-remediation hook
  hook:
    auth:
      url: http://localhost:8080
    name: restart_nginx
    command: sudo systemctl start nginx
    timeout: 60
    stdin: false

- name: Capture the process tree

  hook:
    auth:
      url: http://localhost:8080
    name: process_tree
    command: ps aux
    timeout: 60
    stdin: false
'''

RETURN = '''
object:
    description: object representing Sensu hook
    returned: success
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    arguments, errors, utils,
)


def main():
    required_if = [
        ('state', 'present', ['command', 'timeout'])
    ]
    module = AnsibleModule(
        required_if=required_if,
        supports_check_mode=True,
        argument_spec=dict(
            arguments.get_spec(
                "auth", "name", "state", "labels", "annotations",
            ),
            command=dict(),
            timeout=dict(
                type='int',
            ),
            stdin=dict(
                type='bool'
            ),
            runtime_assets=dict(
                type='list',
            ),
        ),
    )

    client = arguments.get_sensu_client(module.params['auth'])
    path = '/hooks/{0}'.format(module.params['name'])
    payload = arguments.get_mutation_payload(
        module.params, 'command', 'timeout', 'stdin', 'runtime_assets'
    )
    try:
        changed, hook = utils.sync(
            module.params['state'], client, path, payload, module.check_mode,
        )
        module.exit_json(changed=changed, object=hook)
    except errors.Error as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
