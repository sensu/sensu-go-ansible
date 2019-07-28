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
module: sensu_go_entity
author: "Paul Arthur (@flowerysong)"
short_description: Manages Sensu entities
description:
  - 'For more information, refer to the Sensu documentation: U(https://docs.sensu.io/sensu-go/latest/reference/entities/)'
extends_documentation_fragment:
  - flowerysong.sensu_go.base
  - flowerysong.sensu_go.object
options:
  class:
    description:
      - Entity class. Standard classes are 'proxy' and 'agent', but you can use
        whatever you want.
    default: proxy
  subscriptions:
    description:
      - List of subscriptions for the entity.
    type: list
    default: []
  deregister:
    description:
      - Whether automatic deregistration should be enabled.
    type: bool
    default: no
  deregistration_handler:
    description:
      - Handler to call for deregistration events.
'''

EXAMPLES = '''
# Create a proxy entity
- sensu_go_entity:
    name: api.example.com
    subscriptions:
      - tls
    metadata:
      labels:
        Status: production

# Modify an agent entity
- sensu_go_entity:
    name: api-server-01.example.com
    entity_class: agent
    labels:
      Status: outofservice
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.flowerysong.sensu_go.plugins.module_utils.base import SensuObject


class SensuEntity(SensuObject):
    def __init__(self, module):
        super(SensuEntity, self).__init__(module)
        self.path = '/entities/{0}'.format(self.params['name'])
        self.payload.update({
            'entity_class': self.params['class'],
            'subscriptions': self.params['subscriptions'],
            'deregister': self.params['deregister'],
        })

        if self.params['deregistration_handler']:
            self.payload['deregistration'] = {
                'handler': self.params['deregistration_handler'],
            }


def main():
    argspec = SensuEntity.argument_spec()
    argspec.update({
        'class': {
            'default': 'proxy',
            'type': 'str',
        },
        'subscriptions': {
            'type': 'list',
            'default': [],
        },
        'deregister': {
            'default': False,
            'type': 'bool',
        },
        'deregistration_handler': {
            'type': 'str'
        },
    })

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
    )

    entity = SensuEntity(module)
    result = entity.reconcile()

    module.exit_json(changed=result['changed'], entity=result['object'])


if __name__ == '__main__':
    main()
