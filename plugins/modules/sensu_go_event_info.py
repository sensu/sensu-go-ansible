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
module: sensu_go_event_info
author: "Paul Arthur (@flowerysong)"
short_description: Lists Sensu events
description:
  - 'For more information, refer to the Sensu documentation: U(https://docs.sensu.io/sensu-go/latest/reference/events/)'
version_added: 0.1.0
extends_documentation_fragment:
  - sensu.sensu_go.base
options:
  check:
    description:
      - Limit results to a specific check.
      - C(entity) must also be specified.
    type: str
  entity:
    description:
      - Limit results to a specific entity.
    type: str
'''

EXAMPLES = '''
- name: List Sensu events
  sensu_go_event_info:
  register: result

- name: List Sensu events for api.example.com
  sensu_go_event_info:
    entity: api.example.com
  register: result
'''

RETURN = '''
events:
  description: list of Sensu events
  returned: always
  type: list
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.sensu.sensu_go.plugins.module_utils.base import sensu_argument_spec, AnsibleSensuClient


def main():
    argspec = sensu_argument_spec()
    argspec.update(
        dict(
            check=dict(),
            entity=dict(),
        )
    )

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
        required_by={'check': ['entity']},
    )

    client = AnsibleSensuClient(module)

    if module.params['check']:
        result = [client.get('/events/{0}/{1}'.format(module.params['entity'], module.params['check']))]
    elif module.params['entity']:
        result = client.get('/events/{0}'.format(module.params['entity']))
    else:
        result = client.get('/events')

    module.exit_json(changed=False, events=result)


if __name__ == '__main__':
    main()
