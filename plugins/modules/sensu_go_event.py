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
extends_documentation_fragment:
  - flowerysong.sensu_go.base
'''

EXAMPLES = '''
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.flowerysong.sensu_go.plugins.module_utils.base import sensu_argument_spec, AnsibleSensuClient


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
                choices=['proxy', 'agent'],
                default='proxy',
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
            },
            'entity_class': module.params['entity_class'],
        },
        'check': {
            'metadata': {
                'name': module.params['name'],
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
