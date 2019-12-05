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
module: event_info
author:
  - Paul Arthur (@flowerysong)
  - Aljaz Kosir (@aljazkosir)
  - Manca Bizjak (@mancabizjak)
  - Tadej Borovsak (@tadeboro)
short_description: List Sensu events
description:
  - Retrieve recent events that Sensu processed.
  - For more information, refer to the Sensu documentation at
    U(https://docs.sensu.io/sensu-go/latest/reference/events/).
version_added: "1.0"
extends_documentation_fragment:
  - sensu.sensu_go.auth
  - sensu.sensu_go.namespace
seealso:
  - module: event
options:
  check:
    description:
      - Limit results to a specific check.
      - I(entity) must also be specified if this parameter is used.
    type: str
  entity:
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

- name: Filter events by check and entity
  event_info:
    entity: api.example.com
    check: check-cpu
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
    required_by = {'check': ['entity']}
    module = AnsibleModule(
        supports_check_mode=True,
        required_by=required_by,
        argument_spec=dict(
            arguments.get_spec("auth", "namespace"),
            check=dict(),
            entity=dict(),
        ),
    )

    client = arguments.get_sensu_client(module.params['auth'])
    path = utils.build_core_v2_path(
        module.params['namespace'], 'events', module.params['entity'],
        module.params['check'],
    )

    try:
        events = utils.prepare_result_list(utils.get(client, path))
    except errors.Error as e:
        module.fail_json(msg=str(e))

    module.exit_json(changed=False, objects=events)


if __name__ == '__main__':
    main()
