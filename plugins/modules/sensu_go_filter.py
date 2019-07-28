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
module: sensu_go_filter
author: "Paul Arthur (@flowerysong)"
short_description: Manages Sensu filters
description:
  - 'For more information, refer to the Sensu documentation: U(https://docs.sensu.io/sensu-go/latest/reference/filters/)'
extends_documentation_fragment:
  - flowerysong.sensu_go.base
  - flowerysong.sensu_go.object
options:
  action:
    description:
      - Filter action.
    choices: [ 'allow', 'deny' ]
    default: allow
  expressions:
    descripton:
      - Filter expressions.
    type: list
  runtime_assets:
    description:
      - Runtime assets for filter.
    type: list
'''

EXAMPLES = '''
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.flowerysong.sensu_go.plugins.module_utils.base import SensuObject


class SensuFilter(SensuObject):
    def __init__(self, module):
        super(SensuFilter, self).__init__(module)

        self.path = '/filters/{0}'.format(self.params['name'])
        for key in ('action', 'expressions', 'runtime_assets'):
            self.payload[key] = self.params[key]


def main():
    argspec = SensuFilter.argument_spec()
    argspec.update(dict(
        action=dict(
            default='allow',
            choices=['allow', 'deny'],
            type='str',
        ),
        expressions=dict(
            type='list',
        ),
        runtime_assets=dict(
            type='list',
        ),
    ))

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
        required_if=[('state', 'present', ['expressions'])],
    )

    filter = SensuFilter(module)
    result = filter.reconcile()
    module.exit_json(changed=result['changed'], filter=result['object'])


if __name__ == '__main__':
    main()
