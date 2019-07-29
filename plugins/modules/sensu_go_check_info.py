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
module: sensu_go_check_info
author: "Paul Arthur (@flowerysong)"
short_description: Lists Sensu checks
description:
  - 'For more information, refer to the Sensu documentation: U(https://docs.sensu.io/sensu-go/latest/reference/checks/)'
version_added: 0.1.0
extends_documentation_fragment:
  - flowerysong.sensu_go.base
  - flowerysong.sensu_go.info
'''

EXAMPLES = '''
- name: List Sensu checks
  sensu_go_check_info:
  register: result
'''

RETURN = '''
checks:
  description: list of Sensu checks
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
        )
    )

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
    )

    client = AnsibleSensuClient(module)

    if module.params['name']:
        result = [client.get('/checks/{0}'.format(module.params['name']))]
    else:
        result = client.get('/checks')

    module.exit_json(changed=False, checks=result)


if __name__ == '__main__':
    main()
