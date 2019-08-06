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
module: sensu_go_cluster_info
author: "Paul Arthur (@flowerysong)"
short_description: Retrieves Sensu cluster status
description:
  - 'For more information, refer to the Sensu documentation: U(https://docs.sensu.io/sensu-go/latest/reference/backend/)'
version_added: 0.1.0
extends_documentation_fragment:
  - sensu.sensu_go.base
'''

EXAMPLES = '''
- name: Get Sensu cluster information
  sensu_go_cluster_info:
  register: result
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.sensu.sensu_go.plugins.module_utils.base import sensu_argument_spec, AnsibleSensuClient


def main():
    argspec = sensu_argument_spec()

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
    )

    client = AnsibleSensuClient(module)
    client.namespace = None

    result = client.get('/cluster/members')

    module.exit_json(changed=False, cluster=result)


if __name__ == '__main__':
    main()
