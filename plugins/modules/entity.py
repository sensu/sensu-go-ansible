#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Paul Arthur <paul.arthur@flowerysong.com>
# Copyright: (c) 2019, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["stableinterface"],
    "supported_by": "certified",
}

DOCUMENTATION = '''
module: entity
author:
  - Paul Arthur (@flowerysong)
  - Aljaz Kosir (@aljazkosir)
  - Miha Plesko (@miha-plesko)
  - Tadej Borovsak (@tadeboro)
short_description: Manage Sensu entities
description:
  - Create, update or delete Sensu entity.
  - For more information, refer to the Sensu documentation at
    U(https://docs.sensu.io/sensu-go/latest/reference/entities/).
version_added: "1.0"
extends_documentation_fragment:
  - sensu.sensu_go.auth
  - sensu.sensu_go.name
  - sensu.sensu_go.namespace
  - sensu.sensu_go.state
  - sensu.sensu_go.labels
  - sensu.sensu_go.annotations
seealso:
  - module: entity_info
options:
  entity_class:
    description:
      - Entity class. Standard classes are C(proxy) and C(agent), but you can
        use whatever you want.
      - Required if I(state) is C(present).
    type: str
  subscriptions:
    description:
      - List of subscriptions for the entity.
    type: list
    elements: str
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
    elements: str
  user:
    description:
      - Sensu RBAC username used by the entity. Agent entities require get,
        list, create, update, and delete permissions for events across all namespaces.
    type: str
'''

EXAMPLES = '''
- name: Create an entity
  sensu.sensu_go.entity:
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

- name: Delete an entity
  sensu.sensu_go.entity:
    name: entity
    state: absent
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


def do_differ(current, desired):
    system = desired.get('system')
    if system and utils.do_differ(current.get('system'), system):
        return True

    return utils.do_differ(current, desired, 'system')


def main():
    required_if = [
        ('state', 'present', ['entity_class'])
    ]
    module = AnsibleModule(
        required_if=required_if,
        supports_check_mode=True,
        argument_spec=dict(
            arguments.get_spec(
                "auth", "name", "state", "labels", "annotations", "namespace",
            ),
            entity_class=dict(),
            subscriptions=dict(
                type='list', elements='str',
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
                type='list', elements='str',
            ),
            user=dict()
        ),
    )

    client = arguments.get_sensu_client(module.params['auth'])
    path = utils.build_core_v2_path(
        module.params['namespace'], 'entities', module.params['name'],
    )
    payload = arguments.get_mutation_payload(
        module.params, 'entity_class', 'subscriptions', 'system', 'last_seen', 'deregister',
        'redact', 'user'
    )
    if module.params['deregistration_handler']:
        payload['deregistration'] = dict(handler=module.params['deregistration_handler'])
    try:
        changed, entity = utils.sync(
            module.params['state'], client, path, payload, module.check_mode,
            do_differ,
        )
        module.exit_json(changed=changed, object=entity)
    except errors.Error as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
