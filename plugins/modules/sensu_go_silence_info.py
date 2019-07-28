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
module: sensu_go_silence_info
author: "Paul Arthur (@flowerysong)"
short_description: Lists Sensu silence entries
description:
  - 'For more information, refer to the Sensu documentation: U(https://docs.sensu.io/sensu-go/latest/reference/silencing/)'
extends_documentation_fragment:
  - flowerysong.sensu_go.base
  - flowerysong.sensu_go.info
options:
  subscription:
    - Subscription to retrieve silencing entries for.
  check:
    - Check to retrieve silencing entries for.
'''

EXAMPLES = '''
- name: List Sensu silence entrues
  sensu_go_silence_info:
  register: result
'''

RETURN = '''
silence_entries:
  description: list of Sensu silence entries
  returned: always
  type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.flowerysong.sensu_go.plugins.module_utils.base import sensu_argument_spec, AnsibleSensuClient


def main():
    argspec = sensu_argument_spec()
    argspec.update(
        dict(
            name=dict(),
            subscription=dict(),
            check=dict(),
        )
    )

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
        mutually_exclusive=['name', 'subscription', 'check'],
    )

    client = AnsibleSensuClient(module)

    if module.params['subscription']:
        result = client.get('/silenced/subscriptions/{0}'.format(module.params['subscription']))
    elif module.params['check']:
        result = client.get('/silenced/checks/{0}'.format(module.params['check']))
    elif module.params['name']:
        result = [client.get('/silenced/{0}'.format(module.params['name']))]
    else:
        result = client.get('/silenced')

    module.exit_json(changed=False, silenced=result)


if __name__ == '__main__':
    main()
