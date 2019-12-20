#!/usr/bin/python
# -*- coding: utf-8 -*-
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

DOCUMENTATION = """
module: datastore_info
author:
  - Manca Bizjak (@mancabizjak)
  - Tadej Borovsak (@tadeboro)
short_description: List external Sensu datastore providers
description:
  - Retrieve information about external Sensu datastores.
  - For more information, refer to the Sensu documentation at
    U(https://docs.sensu.io/sensu-go/latest/reference/datastore/).
version_added: "1.1"
extends_documentation_fragment:
  - sensu.sensu_go.auth
  - sensu.sensu_go.info
seealso:
  - module: datastore
"""

EXAMPLES = """
- name: List all external Sensu datastores
  datastore_info:
  register: result

- name: Retrieve the selected external Sensu datastore
  datastore_info:
    name: my-datastore
  register: result

- name: Do something with result
  debug:
    msg: "{{ result.objects.0.dsn }}"
"""

RETURN = """
objects:
  description: list of external Sensu datastore providers
  returned: always
  type: list
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    arguments, errors, utils,
)

API_GROUP = "enterprise"
API_VERSION = "store/v1"


def main():
    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=dict(
            arguments.get_spec("auth"),
            name=dict(),  # Name is not required in info modules.
        ),
    )

    client = arguments.get_sensu_client(module.params["auth"])
    path = utils.build_url_path(
        API_GROUP, API_VERSION, None, "provider", module.params["name"],
    )

    try:
        stores = utils.prepare_result_list(utils.get(client, path))
        # We simulate the behavior of v2 API here and only return the spec.
        module.exit_json(changed=False, objects=[s["spec"] for s in stores])
    except errors.Error as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
