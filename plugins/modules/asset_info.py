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
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = """
module: asset_info
author:
  - Paul Arthur (@flowerysong)
  - Aljaz Kosir (@aljazkosir)
  - Miha Plesko (@miha-plesko)
  - Tadej Borovsak (@tadeboro)
short_description: Lists Sensu assets
description:
  - For more information, refer to the Sensu documentation at
    U(https://docs.sensu.io/sensu-go/latest/reference/assets/)
version_added: 0.0.1
extends_documentation_fragment:
  - sensu.sensu_go.auth
  - sensu.sensu_go.info
"""

EXAMPLES = """
- name: List Sensu assets
  asset_info:
  register: result
"""

RETURN = """
objects:
  description: list of Sensu assets
  returned: always
  type: list
"""

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
    if module.params["name"]:
        path = "/assets/{0}".format(module.params["name"])
    else:
        path = "/assets"

    try:
        assets = utils.get(client, path)
    except errors.Error as e:
        module.fail_json(msg=str(e))

    if module.params["name"]:
        assets = [assets]
    module.exit_json(changed=False, objects=assets)


if __name__ == "__main__":
    main()
