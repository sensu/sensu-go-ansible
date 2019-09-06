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
    "supported_by": "community",
}

DOCUMENTATION = """
module: sensu_go_asset
author: "Cameron Hurst (@wakemaster39)"
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
  download_url:
    description:
      - The URL location of the asset.
    type: str
    required: true
  sha512:
    description:
      - The checksum of the asset.
    type: str
    required: true
  filters:
    description:
      - A set of Sensu query expressions used to determine if the asset
        should be installed.
    type: list
    default: []
  headers:
    description:
      - Additional headers to send when retrieving the asset, e.g. for
        authorization.
    type: dict
    default: {}
"""

EXAMPLES = """
- name: Create asset
  sensu_go_asset:
    name: asset
    download_url: https://assets.bonsai.sensu.io/68546e739d96fd695655b77b35b5aabfbabeb056/sensu-plugins-cpu-checks_4.0.0_centos_linux_amd64.tar.gz
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
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    arguments, errors, utils,
)


def main():
    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=dict(
            arguments.MUTATION_ARGUMENTS,
            download_url=dict(
                required=True,
            ),
            sha512=dict(
                required=True,
            ),
            filters=dict(
                type="list",
                default=[],
            ),
            headers=dict(
                type="dict",
                default={},
            ),
        ),
    )

    client = arguments.get_sensu_client(module.params)
    path = "/assets/{0}".format(module.params["name"])
    payload = arguments.get_mutation_payload(
        module.params, "download_url", "sha512", "filters", "headers",
    )
    payload["url"] = payload.pop("download_url")  # Remap download_url -> url

    try:
        changed, asset = utils.sync(
            module.params["state"], client, path, payload, module.check_mode,
        )
        module.exit_json(changed=changed, asset=asset)
    except errors.Error as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
