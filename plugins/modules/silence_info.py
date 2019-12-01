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
module: silence_info
author:
  - Paul Arthur (@flowerysong)
  - Aljaz Kosir (@aljazkosir)
  - Manca Bizjak (@mancabizjak)
  - Tadej Borovsak (@tadeboro)
short_description: List Sensu silence entries
description:
  - Retrieve information about Sensu silences.
  - For more information, refer to the Sensu documentation at
    U(https://docs.sensu.io/sensu-go/latest/reference/silencing/).
extends_documentation_fragment:
  - sensu.sensu_go.auth
options:
  subscription:
    description:
      - The name of the subscription the entry should match. If left empty a silencing entry will
        contain an asterisk in the subscription position.
    type: str
  check:
    description:
     - The name of the check the entry should match. If left empty a silencing entry will contain an
       asterisk in the check position.
    type: str
'''

EXAMPLES = '''
- name: List Sensu silence entries
  silence_info:
  register: result

- name: Fetch specific silence with name proxy:awesome_check
  silence_info:
    subscription: proxy
    check: awesome_check
  register: result
'''

RETURN = '''
objects:
  description: list of Sensu silence entries
  returned: always
  type: list
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    arguments, errors, utils
)


def main():
    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=dict(
            arguments.get_spec('auth'),
            subscription=dict(),
            check=dict(),
        ),
    )

    name = '{0}:{1}'.format(module.params['subscription'] or '*', module.params['check'] or '*')
    client = arguments.get_sensu_client(module.params["auth"])
    path = utils.build_url_path("silenced", None if name == "*:*" else name)

    try:
        silences = utils.get(client, path)
    except errors.Error as e:
        module.fail_json(msg=str(e))

    if name != '*:*':
        silences = [silences]
    module.exit_json(changed=False, objects=silences)


if __name__ == '__main__':
    main()
