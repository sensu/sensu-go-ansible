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
module: sensu_go_backend_info
author: "Paul Arthur (@flowerysong)"
short_description: Retrieves Sensu backend status
description:
  - 'For more information, refer to the Sensu documentation: U(https://docs.sensu.io/sensu-go/latest/reference/backend/)'
version_added: 0.1.0
extends_documentation_fragment:
  - flowerysong.sensu_go.base
'''

EXAMPLES = '''
- name: Get Sensu backend information
  sensu_go_backend_info:
  register: result
'''

RETURN = '''
'''

import json

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.dict_transformations import camel_dict_to_snake_dict
from ansible.module_utils.urls import open_url
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError

from ansible_collections.flowerysong.sensu_go.plugins.module_utils.base import sensu_argument_spec


def main():
    argspec = sensu_argument_spec()

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
    )

    url = module.params['url'].rstrip('/')

    backend = {}
    for endpoint in 'health', 'version':
        try:
            result = open_url('{0}/{1}'.format(url, endpoint))
        except (HTTPError, URLError) as e:
            module.fail_json(msg='get failed: {0} {1}'.format(e.reason, e.read()))

        backend[endpoint] = camel_dict_to_snake_dict(json.loads(result.read()))

    module.exit_json(changed=False, backend=backend)


if __name__ == '__main__':
    main()
