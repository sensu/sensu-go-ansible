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
module: bonsai_asset
author:
  - Aljaz Kosir (@aljazkosir)
  - Manca Bizjak (@mancabizjak)
  - Tadej Borovsak (@tadeboro)
short_description: Add Sensu assets from Bonsai
description:
  - Create or update a Sensu Go asset whose definition is available in the
    Bonsai, the Sensu asset index.
  - For more information, refer to the Sensu documentation at
    U(https://docs.sensu.io/sensu-go/latest/reference/assets/)
    and U(https://bonsai.sensu.io/)
version_added: "1.0"
extends_documentation_fragment:
  - sensu.sensu_go.auth
  - sensu.sensu_go.name
  - sensu.sensu_go.namespace
  - sensu.sensu_go.labels
  - sensu.sensu_go.annotations
options:
  version:
    description:
      - Version number of the asset to install.
    type: str
    required: true
  rename:
    description:
      - The name that will be used when adding the asset to Sensu.
      - If not present, value of the I(name) parameter will be used.
    type: str
notes:
  - I(labels) and I(annotations) values are merged with the values obtained
    from Bonsai. Values passed-in as parameters take precedence over the
    values obtained from Bonsai.
  - To delete an asset, use regular M(asset) module.
seealso:
  - module: asset
  - module: asset_info
"""

EXAMPLES = """
- name: Make sure specific version of asset is installed
  sensu.sensu_go.bonsai_asset:
    name: sensu/monitoring-plugins
    version: 2.2.0-1

- name: Remove previously added asset
  asset:
    name: sensu/monitoring-plugins
    state: absent

- name: Store Bonsai asset under a different name
  sensu.sensu_gobonsai_asset:
    name: sensu/monitoring-plugins
    version: 2.2.0-1
    rename: sensu-monitoring-2.2.0-1

- name: Display asset info
  asset_info:
    name: sensu-monitoring-2.2.0-1  # value from rename field
"""

RETURN = """
object:
    description: object representing Sensu asset
    returned: success
    type: dict
"""
