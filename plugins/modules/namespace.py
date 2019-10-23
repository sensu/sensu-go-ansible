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
module: namespace
author:
  - Paul Arthur (@flowerysong)
  - Aljaz Kosir (@aljazkosir)
  - Miha Plesko (@miha-plesko)
  - Tadej Borovsak (@tadeboro)
short_description: Manages Sensu namespaces
description:
  - For more information, refer to the Sensu documentation at
    U(https://docs.sensu.io/sensu-go/latest/reference/rbac/#namespaces)
extends_documentation_fragment:
  - sensu.sensu_go.auth
  - sensu.sensu_go.name
  - sensu.sensu_go.state
notes:
  - Parameter C(auth.namespace) is ignored in this module.
'''

EXAMPLES = '''
- name: Create a new namespace
  namespace:
    name: production
    state: present

- name: Delete a namespace
  namespace:
    name: staging
    state: absent
'''

RETURN = '''
object:
    description: object representing Sensu namespace
    returned: success
    type: dict
'''


from ansible.module_utils.basic import AnsibleModule, env_fallback


from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    arguments, errors, utils,
)


def main():
    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=arguments.get_spec("auth", "name", "state"),
    )
    module.params['auth']['namespace'] = None
    client = arguments.get_sensu_client(module.params['auth'])
    path = '/namespaces/{0}'.format(module.params['name'])
    payload = arguments.get_spec_payload(
        module.params, 'name'
    )
    try:
        changed, namespace = utils.sync(
            module.params['state'], client, path, payload, module.check_mode,
        )
        module.exit_json(changed=changed, object=namespace)
    except errors.Error as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
