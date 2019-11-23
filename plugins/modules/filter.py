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
module: filter
author:
  - Paul Arthur (@flowerysong)
  - Aljaz Kosir (@aljazkosir)
  - Miha Plesko (@miha-plesko)
  - Tadej Borovsak (@tadeboro)
short_description: Manages Sensu filters
description:
  - For more information, refer to the Sensu documentation at
    U(https://docs.sensu.io/sensu-go/latest/reference/filters/)
extends_documentation_fragment:
  - sensu.sensu_go.auth
  - sensu.sensu_go.name
  - sensu.sensu_go.state
  - sensu.sensu_go.labels
  - sensu.sensu_go.annotations
options:
  action:
    description:
      - Action to take with the event if the filter expressions match.
    type: str
    choices: [ 'allow', 'deny' ]
  expressions:
    description:
      - Filter expressions to be compared with event data.
    type: list
  runtime_assets:
    description:
      - Assets to be applied to the filter's execution context.
        JavaScript files in the lib directory of the asset will be evaluated.
    type: list
'''

EXAMPLES = '''
- name: Create a filter
  filter:
    name: filter
    action: deny
    expressions:
      - event.check.interval == 10
      - event.check.occurrences == 1
    runtime_assets: awesomeness

- name: Create a production filter
  filter:
    name: filter
    action: allow
    expressions:
      - event.entity.labels['environment'] == 'production'

- name: Create a filter with JS expression
  filter:
    name: filter
    action: deny
    expressions:
      - "_.reduce(event.check.history, function(memo, h) { return (memo || h.status != 0); })"
    runtime_assets:
      - underscore

- name: Handling repeated events
  filter:
    name: filter_interval_60_hourly
    action: allow
    expressions:
      - event.check.interval == 60
      - event.check.occurrences == 1 || event.check.occurrences % 60 == 0
'''

RETURN = '''
object:
    description: object representing Sensu filter
    returned: success
    type: dict
'''


from ansible.module_utils.basic import AnsibleModule

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    arguments, errors, utils,
)


def main():
    required_if = [
        ('state', 'present', ['action', 'expressions'])
    ]
    module = AnsibleModule(
        required_if=required_if,
        supports_check_mode=True,
        argument_spec=dict(
            arguments.get_spec(
                "auth", "name", "state", "labels", "annotations",
            ),
            action=dict(choices=['allow', 'deny']),
            expressions=dict(
                type='list',
            ),
            runtime_assets=dict(
                type='list',
            ),
        ),
    )

    client = arguments.get_sensu_client(module.params['auth'])
    path = utils.build_url_path('filters', module.params['name'])
    payload = arguments.get_mutation_payload(
        module.params, 'action', 'expressions', 'runtime_assets'
    )
    try:
        changed, sensu_filter = utils.sync(
            module.params['state'], client, path, payload, module.check_mode,
        )
        module.exit_json(changed=changed, object=sensu_filter)
    except errors.Error as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
