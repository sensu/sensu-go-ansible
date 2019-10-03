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
module: event_info
author:
  - Paul Arthur (@flowerysong)
  - Aljaz Kosir (@aljazkosir)
  - Miha Plesko (@miha-plesko)
  - Tadej Borovsak (@tadeboro)
short_description: Lists Sensu events
description:
  - For more information, refer to the Sensu documentation at
    U(https://docs.sensu.io/sensu-go/latest/reference/events/)
extends_documentation_fragment:
  - sensu.sensu_go.base
options:
  check_name:
    description:
      - Limit results to a specific check.
      - C(entity) must also be specified.
    type: str
  entity_name:
    description:
      - Limit results to a specific entity.
    type: str
'''

EXAMPLES = '''
- name: List Sensu events
  event_info:
  register: result

- name: List Sensu events for api.example.com
  event_info:
    entity: api.example.com
  register: result
'''

RETURN = '''
objects:
  description: list of Sensu events
  returned: always
  type: list
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    arguments, errors, utils,
)


def main():
    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=dict(
            arguments.COMMON_ARGUMENTS,
            check_name=dict(),
            entity_name=dict(),
        ),
    )
    if module.params['check_name'] and not module.params['entity_name']:
        module.fail_json(msg='check_name is present but entity_name is missing')

    client = arguments.get_sensu_client(module.params['auth'])
    if module.params['check_name']:
        path = '/events/{0}/{1}'.format(module.params['entity_name'], module.params['check_name'])
    elif module.params['entity_name']:
        path = '/events/{0}'.format(module.params['entity_name'])
    else:
        path = '/events'

    try:
        events = utils.get(client, path)
    except errors.Error as e:
        module.fail_json(msg=str(e))

    if module.params['check_name']:
        events = [events]
    module.exit_json(changed=False, objects=events)


if __name__ == '__main__':
    main()
