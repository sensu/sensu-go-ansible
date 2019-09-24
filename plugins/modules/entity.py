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
                    'supported_by': 'XLAB community'}

DOCUMENTATION = '''
module: entity
author:
  - Paul Arthur (@flowerysong)
  - Aljaz Kosir (@aljazkosir)
  - Miha Plesko (@miha-plesko)
  - Tadej Borovsak (@tadeboro)
short_description: Manages Sensu entities
description:
  - For more information, refer to the Sensu documentation at
    U(https://docs.sensu.io/sensu-go/latest/reference/entities/)
extends_documentation_fragment:
  - sensu.sensu_go.base
  - sensu.sensu_go.object
options:
  entity_class:
    description:
      - Entity class. Standard classes are 'proxy' and 'agent', but you can use
        whatever you want.
    type: str
  subscriptions:
    description:
      - List of subscriptions for the entity.
    type: list
  system:
    description:
      - System information about the entity, such as operating system and platform. See
        U(https://docs.sensu.io/sensu-go/5.13/reference/entities/#system-attributes) for more information.
    type: dict
  last_seen:
    description:
      - Timestamp the entity was last seen, in seconds since the Unix epoch.
    type: int
  deregister:
    description:
      - If the entity should be removed when it stops sending keepalive messages.
    type: bool
  deregistration_handler:
    description:
      - The name of the handler to be called when an entity is deregistered.
    type: str
  redact:
    description:
      - List of items to redact from log messages. If a value is provided,
        it overwrites the default list of items to be redacted.
    type: list
  user:
    description:
      - Sensu RBAC username used by the entity. Agent entities require get,
        list, create, update, and delete permissions for events across all namespaces.
    type: str
'''

EXAMPLES = '''
- name: Create entity
  entity:
    auth:
      url: http://localhost:8080
    name: entity
    entity_class: proxy
    subscriptions:
      - web
      - prod
    system:
      hostname: playbook-entity
      os: linux
      platform: ubutntu
      network:
        interfaces:
          - name: lo
            addresses:
              - 127.0.0.1/8
              - ::1/128
          - name: eth0
            mac: 52:54:00:20:1b:3c
            addresses:
              - 93.184.216.34/24
    last_seen: 1522798317
    deregister: yes
    deregistration_handler: email-handler
    redact:
      - password
      - pass
      - api_key
    user: agent
'''

RETURN = '''
object:
    description: object representing Sensu entity
    returned: success
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    arguments, errors, utils,
)


def main():
    required_if = [
        ('state', 'present', ['entity_class'])
    ]
    module = AnsibleModule(
        required_if=required_if,
        supports_check_mode=True,
        argument_spec=dict(
            arguments.MUTATION_ARGUMENTS,
            entity_class=dict(),
            subscriptions=dict(
                type='list',
            ),
            system=dict(
                type='dict'
            ),
            last_seen=dict(
                type='int'
            ),
            deregister=dict(
                type='bool'
            ),
            deregistration_handler=dict(),
            redact=dict(
                type='list'
            ),
            user=dict()
        ),
    )

    client = arguments.get_sensu_client(module.params['auth'])
    path = '/entities/{0}'.format(module.params['name'])
    payload = arguments.get_mutation_payload(
        module.params, 'entity_class', 'subscriptions', 'system', 'last_seen', 'deregister',
        'redact', 'user'
    )
    if module.params['deregistration_handler']:
        payload['deregistration'] = dict(handler=module.params['deregistration_handler'])
    try:
        changed, entity = utils.sync(
            module.params['state'], client, path, payload, module.check_mode,
        )
        module.exit_json(changed=changed, object=entity)
    except errors.Error as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
