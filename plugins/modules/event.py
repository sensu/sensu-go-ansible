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
module: event
author:
  - Paul Arthur (@flowerysong)
  - Aljaz Kosir (@aljazkosir)
  - Miha Plesko (@miha-plesko)
  - Tadej Borovsak (@tadeboro)
short_description: Manages Sensu hooks
description:
  - For more information, refer to the Sensu documentation at
    U(https://docs.sensu.io/sensu-go/latest/reference/events/)
extends_documentation_fragment:
  - sensu.sensu_go.base
options:
  timestamp:
    description:
      - Time that the event occurred in seconds since the Unix epoch.
    type: int
  state:
    description:
      - Target state of the Sensu object.
    type: str
    choices: [ 'present', 'absent' ]
    default: present
  entity:
    description:
      - Entity object returned from M(entity) or M(entity_info).
    type: dict
  check:
    description:
      - Check object returned from M(check) or M(check_info).
    type: dict
  check_merge:
    description:
      - Information about the status and history of the event.
        U(https://docs.sensu.io/sensu-go/latest/reference/events/#check-attributes)
    type: dict
    suboptions:
      duration:
        description: Command execution time in seconds.
        type: float
      executed:
        description: Time that the check request was executed.
        type: int
      history:
        description: Check status history for the last 21 check executions.
        type: list
      issued:
        description: Time that the check request was issued in seconds since the Unix epoch.
        type: int
      last_ok:
        description: The last time that the check returned an OK status (0) in seconds since the Unix epoch.
        type: int
      output:
        description: The output from the execution of the check command.
        type: str
      state:
        description: The state of the check.
        choices: [ "passing", "failing", "flapping" ]
        type: str
      status:
        description: Exit status code produced by the check.
        choices: [ "ok", "warning", "critical", "unknown" ]
        type: str
      total_state_change:
        description: The total state change percentage for the check's history.
        type: int
'''

EXAMPLES = '''
- name: Create a simple entity
  entity:
    auth:
      url: http://localhost:8080
    name: awesome_entity
    entity_class: proxy
  register: entity

- name: Create a simple check
  check:
    auth:
      url: http://localhost:8080
    name: awesome_check
    command: echo "Hello world"
    subscriptions:
      - checks
      - also_checks
    interval: 30
  register: check

- name: Create event with minimal parameters
  event:
    auth:
      url: http://localhost:8080
    entity: "{{ entity.object }}"
    check: "{{ check.object }}"
    check_merge:
      output: Hello world
'''

RETURN = '''
object:
  description: object representing Sensu event
  returned: always
  type: list
'''

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    arguments, errors, utils
)


def main():
    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=dict(
            arguments.COMMON_ARGUMENTS,
            state=dict(
                default='present',
                choices=['present', 'absent'],
            ),
            timestamp=dict(type='int'),
            entity=dict(type='dict'),
            check=dict(type='dict'),
            check_merge=dict(
                type='dict',
                options=dict(
                    duration=dict(
                        type='float'
                    ),
                    executed=dict(
                        type='int'
                    ),
                    history=dict(
                        type='list'
                    ),
                    issued=dict(
                        type='int'
                    ),
                    last_ok=dict(
                        type='int'
                    ),
                    output=dict(),
                    state=dict(
                        choices=['passing', 'failing', 'flapping']
                    ),
                    status=dict(
                        choices=['ok', 'warning', 'critical', 'unknown']
                    ),
                    total_state_change=dict(
                        type='int'
                    )
                )
            )
        )
    )

    status_map = {
        'ok': 0,
        'warning': 1,
        'critical': 2,
        'unknown': 3,
    }

    client = arguments.get_sensu_client(module.params['auth'])
    path = '/events/{0}/{1}'.format(module.params['entity']['metadata']['name'],
                                    module.params['check']['metadata']['name'])

    payload = arguments.get_spec_payload(module.params, 'timestamp', 'entity', 'check', 'metrics')

    payload['metadata'] = dict(
        namespace=module.params['auth']['namespace']
    )
    if module.params['check_merge']:
        payload['check'].update(module.params['check_merge'])
        if module.params['check_merge'].get('status'):
            payload['check']['status'] = status_map[payload['check']['status']]

    try:
        changed, hook = utils.sync(
            module.params['state'], client, path, payload, module.check_mode
        )
        module.exit_json(changed=changed, object=hook)
    except errors.Error as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
