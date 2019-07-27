# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Paul Arthur <paul.arthur@flowerysong.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


class ModuleDocFragment(object):
    DOCUMENTATION = """
options:
  name:
    description:
      - The Sensu object's name.
    required: yes
  state:
    description:
      - Target state of the Sensu object.
    choices: [ 'present', 'absent' ]
    default: present
  labels:
    description:
      - Custom metadata fields that can be accessed within Sensu, as key/value pairs.
    type: dict
  annotations:
    description:
      - Custom metadata fields with fewer restrictions, as key/value pairs.
      - These are preserved by Sensu but not accessible as tokens or identifiers, and are mainly intended for use with external tools.
    type: dict
"""
