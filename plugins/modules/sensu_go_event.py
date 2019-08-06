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
module: sensu_go_event
author: "Paul Arthur (@flowerysong)"
short_description: Manages Sensu events
description:
  - 'For more information, refer to the Sensu documentation: U(https://docs.sensu.io/sensu-go/latest/reference/events/)'
version_added: 0.1.0
extends_documentation_fragment:
  - sensu.sensu_go.base
  - sensu.sensu_go.object
options:
  entity:
    description:
      - Name of the entity associated with this event.
    type: str
    required: true
  entity_class:
    description:
      - Class the entity belongs to.
      - The standard classes are 'proxy' and 'agent'.
    type: str
    default: proxy
    aliases: ['class']
  entity_annotations:
    description:
      - C(annotations) for the entity associated with this event.
    type: dict
    default: {}
  entity_labels:
    description:
      - C(labels) for the entity associated with this event.
    type: dict
    default: {}
  interval:
    description:
      - Interval the check runs at. I don't know why this is useful for ad-hoc events, but it is required by the API.
    type: int
    default: 60
  output:
    description:
      - Event output.
    type: str
  status:
    description:
      - Event status.
    type: str
    choices: ['ok', 'warning', 'critical', 'unknown']
    default: ok
  duration:
    description:
      - Amount of time the check ran for.
    type: float
    default: 0.0
  handlers:
    description:
      - Handlers for this event.
    type: list
    default: []
'''

EXAMPLES = '''
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.sensu.sensu_go.plugins.module_utils.base import clean_metadata_dict, sensu_argument_spec, AnsibleSensuClient


def main():
    argspec = sensu_argument_spec()
    argspec.update(
        dict(
            name=dict(
                required=True,
            ),
            state=dict(
                choices=['present', 'absent'],
                default='present',
            ),
            entity=dict(
                required=True,
            ),
            entity_class=dict(
                default='proxy',
                aliases=['class'],
            ),
            interval=dict(
                type='int',
                default=60,
            ),
            output=dict(),
            status=dict(
                default='ok',
                choices=['ok', 'warning', 'critical', 'unknown'],
            ),
            duration=dict(
                type='float',
                default=0.0,
            ),
            handlers=dict(
                type='list',
                default=[],
            ),
            labels=dict(
                type='dict',
                default={},
            ),
            annotations=dict(
                type='dict',
                default={},
            ),
            entity_labels=dict(
                type='dict',
                default={},
            ),
            entity_annotations=dict(
                type='dict',
                default={},
            ),
        )
    )

    module = AnsibleModule(
        supports_check_mode=False,
        argument_spec=argspec,
    )

    client = AnsibleSensuClient(module)
    url = '/events/{0}/{1}'.format(module.params['entity'], module.params['name'])

    if module.params['state'] == 'absent':
        client.delete(url)
        module.exit_json(changed=True)

    status_map = {
        'ok': 0,
        'warning': 1,
        'critical': 2,
        'unknown': 3,
    }

    payload = {
        'entity': {
            'metadata': {
                'name': module.params['entity'],
                'namespace': module.params['namespace'],
                'annotations': clean_metadata_dict(module.params['entity_annotations']),
                'labels': clean_metadata_dict(module.params['entity_labels']),
            },
            'entity_class': module.params['entity_class'],
        },
        'check': {
            'metadata': {
                'name': module.params['name'],
                'annotations': clean_metadata_dict(module.params['annotations']),
                'labels': clean_metadata_dict(module.params['labels']),
            },
            'interval': module.params['interval'],
            'status': status_map[module.params['status']],
            'duration': module.params['duration'],
            'output': module.params['output'],
        },
    }

    if module.params['handlers']:
        payload['check']['handlers'] = module.params['handlers']

    client.put(url, payload)
    module.exit_json(changed=True, event=payload)


if __name__ == '__main__':
    main()
