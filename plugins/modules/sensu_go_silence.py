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
module: sensu_go_silence
author: "Paul Arthur (@flowerysong)"
short_description: Manages Sensu silences
description:
  - 'For more information, refer to the Sensu documentation: U(https://docs.sensu.io/sensu-go/latest/reference/silences/)'
version_added: 0.1.0
extends_documentation_fragment:
  - sensu.sensu_go.base
  - sensu.sensu_go.object
options:
  name:
    description:
      - Silence name, in the form 'subscription:check_name'.
  begin:
    description:
      - Unix epoch time when the silence should take effect.
    type: int
  expire:
    description:
      - Number of seconds until the silence expires
    type: int
    default: -1
  expire_on_resolve:
    description:
      - Remove the silence entry when a check returns OK.
    type: bool
    default: false
  reason:
    description:
      - Reason for silencing.
    type: str
'''

EXAMPLES = '''
- name: Silence a specific check
  sensu_go_silence:
    name: Class_mx:check-disk

- name: Silence all checks on a specific host
  sensu_go_silence:
    name: entity:punk-zenfusho.mx.x.mail.umich.edu:*
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.sensu.sensu_go.plugins.module_utils.base import SensuObject


class SensuSilence(SensuObject):
    def __init__(self, module):
        super(SensuSilence, self).__init__(module)

        self.path = '/silenced/{0}'.format(self.params['name'])
        for key in ('begin', 'expire', 'expire_on_resolve', 'reason'):
            if self.params[key] is not None:
                self.payload[key] = self.params[key]

        (sub, check) = self.params['name'].rsplit(':', 1)
        self.payload['subscription'] = sub
        self.payload['check'] = check


def main():
    argspec = SensuSilence.argument_spec()
    argspec.update(dict(
        begin=dict(type='int'),
        expire=dict(
            type='int',
            default=-1,
        ),
        expire_on_resolve=dict(
            type='bool',
            default=False,
        ),
        reason=dict(),
    ))

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
    )

    if ':' not in module.params['name']:
        module.fail_json(msg="name must be in the form 'subscription:check_name'")

    silence = SensuSilence(module)
    result = silence.reconcile()
    module.exit_json(changed=result['changed'], silence=result['object'])


if __name__ == '__main__':
    main()
