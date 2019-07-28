#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Cameron Hurst <cahurst@cisco.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
module: sensu_go_asset
author: "Cameron Hurst (@wakemaster39)"
short_description: Manages Sensu assets
description:
  - 'For more information, refer to the Sensu documentation: U(https://docs.sensu.io/sensu-go/latest/reference/assets/)'
extends_documentation_fragment:
  - flowerysong.sensu_go.base
  - flowerysong.sensu_go.object
options:
  state:
    description:
      - Target state of the Sensu object.
    choices: [ 'present' ]
    default: present
  download_url:
    description:
      - The URL location of the asset.
    required: true
  sha512:
    description:
      - The checksum of the asset.
    required: true
  filters:
    description:
      - A set of Sensu query expressions used to determine if the asset should be installed.
    type: list
    default: []
  headers:
    description:
      - Additional headers to send when retrieving the asset, e.g. for authorization.
    type: dict
    default: {}
'''

EXAMPLES = '''
- name: create asset
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
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.flowerysong.sensu_go.plugins.module_utils.base import SensuObject


class SensuAsset(SensuObject):
    def __init__(self, module):
        super(SensuAsset, self).__init__(module)

        self.path = '/assets/{0}'.format(self.params['name'])

        for key in (
            'download_url',
            "sha512",
            "filters",
            "headers"
        ):
            if self.params[key] is not None:
                if key == "download_url":
                    self.payload["url"] = self.params[key]
                else:
                    self.payload[key] = self.params[key]


def main():
    argspec = SensuAsset.argument_spec()
    argspec.update(
        dict(
            state=dict(
                default='present',
                choices=['present'],
            ),
            download_url=dict(
                required=True,
            ),
            sha512=dict(
                required=True,
            ),
            filters=dict(
                type='list',
                default=[],
            ),
            headers=dict(
                type='dict',
                default={},
            ),
        )
    )

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=argspec,
    )

    asset = SensuAsset(module)
    result = asset.reconcile()
    module.exit_json(changed=result['changed'], asset=result['object'])


if __name__ == '__main__':
    main()
