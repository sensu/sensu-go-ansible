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
module: hook_info
author:
  - Paul Arthur (@flowerysong)
  - Aljaz Kosir (@aljazkosir)
  - Miha Plesko (@miha-plesko)
  - Tadej Borovsak (@tadeboro)
short_description: List Sensu hooks
description:
  - Retrieve information about Sensu hooks.
  - For more information, refer to the Sensu documentation at
    U(https://docs.sensu.io/sensu-go/latest/reference/hooks/).
version_added: "1.0"
extends_documentation_fragment:
  - sensu.sensu_go.auth
  - sensu.sensu_go.info
'''

EXAMPLES = '''
- name: List Sensu hooks
  hook_info:
  register: result

- name: Fetch Sensu hook
  hook_info:
    name: awesome-hook
  register: result
'''

RETURN = '''
objects:
  description: list of Sensu hooks
  returned: always
  type: list
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    arguments, errors, utils,
)


def main():
    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=dict(
            arguments.get_spec("auth"),
            name=dict(),  # Name is not required in info modules.
        ),
    )

    client = arguments.get_sensu_client(module.params["auth"])
    path = utils.build_url_path("hooks", module.params["name"])

    try:
        hooks = utils.prepare_result_list(utils.get(client, path))
    except errors.Error as e:
        module.fail_json(msg=str(e))

    module.exit_json(changed=False, objects=hooks)


if __name__ == '__main__':
    main()
