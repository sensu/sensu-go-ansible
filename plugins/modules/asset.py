#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Cameron Hurst <cahurst@cisco.com>
# Copyright: (c) 2019, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "XLAB Steampunk",
}

DOCUMENTATION = """
module: asset
author:
  - Cameron Hurst (@wakemaster39)
  - Aljaz Kosir (@aljazkosir)
  - Miha Plesko (@miha-plesko)
  - Tadej Borovsak (@tadeboro)
short_description: Manages Sensu assets
description:
  - For more information, refer to the Sensu documentation at
    U(https://docs.sensu.io/sensu-go/latest/reference/assets/)
version_added: 0.1.0
extends_documentation_fragment:
  - sensu.sensu_go.base
  - sensu.sensu_go.object
options:
  state:
    description:
      - Target state of the Sensu object.
    type: str
    choices: [ "present", "absent" ]
    default: present
  url:
    description:
      - The URL location of the asset.
    type: str
  sha512:
    description:
      - The checksum of the asset.
    type: str
  filters:
    description:
      - A set of Sensu query expressions used to determine if the asset
        should be installed.
    type: list
  headers:
    description:
      - Additional headers to send when retrieving the asset, e.g. for
        authorization.
    type: dict
"""

EXAMPLES = """
- name: Create asset
  asset:
    name: asset
    url: https://assets.bonsai.sensu.io/68546e739d96fd695655b77b35b5aabfbabeb056/sensu-plugins-cpu-checks_4.0.0_centos_linux_amd64.tar.gz
    sha512: 518e7c17cf670393045bff4af318e1d35955bfde166e9ceec2b469109252f79043ed133241c4dc96501b6636a1ec5e008ea9ce055d1609865635d4f004d7187b
    filters:
      - "entity.system.os == 'linux'"
      - "entity.system.arch == 'amd64'"
      - "entity.system.platform == 'rhel'"
    annotations:
      sensio.io.bonsai.url: https://assets.bonsai.sensu.io/68546e739d96fd695655b77b35b5aabfbabeb056/sensu-plugins-cpu-checks_4.0.0_centos_linux_amd64.tar.gz
      sensio.io.bonsai.tier: Community
      sensio.io.bonsai.version: 4.0.0
      sensio.io.bonsai.tags: ruby-runtime-2.4.4
"""

RETURN = """
object:
    description: object representing Sensu asset
    returned: success
    type: dict
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    arguments, errors, utils,
)


def main():
    required_if = [
        ("state", "present", ["url", "sha512"])
    ]
    module = AnsibleModule(
        required_if=required_if,
        supports_check_mode=True,
        argument_spec=dict(
            arguments.get_spec(
                "auth", "name", "state", "labels", "annotations",
            ),
            url=dict(),
            sha512=dict(),
            filters=dict(
                type="list",
            ),
            headers=dict(
                type="dict",
            ),
        ),
    )

    client = arguments.get_sensu_client(module.params["auth"])
    path = "/assets/{0}".format(module.params["name"])
    payload = arguments.get_mutation_payload(
        module.params, "url", "sha512", "filters", "headers",
    )
    try:
        changed, asset = utils.sync(
            module.params["state"], client, path, payload, module.check_mode,
        )
        module.exit_json(changed=changed, object=asset)
    except errors.Error as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
