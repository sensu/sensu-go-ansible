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
module: user
author:
  - Paul Arthur (@flowerysong)
  - Aljaz Kosir (@aljazkosir)
  - Tadej Borovsak (@tadeboro)
short_description: Manage Sensu users
description:
  - Create, update, activate or deactivate Sensu user.
  - For more information, refer to the Sensu documentation at
    U(https://docs.sensu.io/sensu-go/latest/reference/rbac/#users).
version_added: "1.0"
extends_documentation_fragment:
  - sensu.sensu_go.auth
  - sensu.sensu_go.name
seealso:
  - module: user_info
options:
  state:
    description:
      - Desired state of the user.
      - Users cannot actually be deleted, only deactivated.
    type: str
    choices: [ enabled, disabled ]
    default: enabled
  password:
    description:
      - Password for the user.
      - Required if user with a desired name does not exist yet on the backend.
    type: str
  groups:
    description:
      - List of groups user belongs to.
    type: list
    elements: str
'''

EXAMPLES = '''
- name: Create a user
  user:
    auth:
      url: http://localhost:8080
    name: awesome_username
    password: hidden_password?
    groups:
      - dev
      - prod

- name: Deactivate a user
  user:
    name: awesome_username
    state: disabled
'''

RETURN = '''
object:
    description: object representing Sensu user
    returned: success
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    arguments, errors, utils,
)


def update_password(client, path, username, password, check_mode):
    # Hit the auth testing API and try to validate the credentials. If the API
    # says they are invalid, we need to update them.
    if client.validate_auth_data(username, password):
        return False

    if not check_mode:
        utils.put(client, path + '/password', dict(
            username=username, password=password,
        ))

    return True


def update_groups(client, path, old_groups, new_groups, check_mode):
    to_delete = set(old_groups).difference(new_groups)
    to_add = set(new_groups).difference(old_groups)

    if not check_mode:
        # Next few lines are far from atomic, which means that we can leave a
        # user in any of the intermediate states, but this is the best we can
        # do given the API limitations.
        for g in to_add:
            utils.put(client, path + '/groups/' + g, None)
        for g in to_delete:
            utils.delete(client, path + '/groups/' + g)

    return len(to_delete) + len(to_add) > 0


def update_state(client, path, old_disabled, new_disabled, check_mode):
    changed = old_disabled != new_disabled

    if not check_mode and changed:
        if new_disabled:  # `state: disabled` input parameter
            utils.delete(client, path)
        else:  # `state: enabled` input parameter
            utils.put(client, path + '/reinstate', None)

    return changed


def sync(remote_object, client, path, payload, check_mode):
    # Create new user (either enabled or disabled)
    if remote_object is None:
        if check_mode:
            return True, payload
        utils.put(client, path, payload)
        return True, utils.get(client, path)

    # Update existing user. We do this on a field-by-field basis because the
    # upsteam API for updating users requires a password field to be set. Of
    # course, we do not want to force users to specify an existing password
    # just for the sake of updating the group membership, so this is why we
    # use field-specific API endpoints to update the user data.

    changed = False
    if 'password' in payload:
        changed = update_password(
            client, path, payload['username'], payload['password'],
            check_mode,
        ) or changed

    if 'groups' in payload:
        changed = update_groups(
            client, path, remote_object.get('groups') or [],
            payload['groups'], check_mode,
        ) or changed

    if 'disabled' in payload:
        changed = update_state(
            client, path, remote_object['disabled'], payload['disabled'],
            check_mode,
        ) or changed

    if check_mode:
        # Backend does not return back passwords, so we should follow the
        # example set by the backend API.
        return changed, dict(
            remote_object,
            **{k: v for k, v in payload.items() if k != 'password'}
        )

    return changed, utils.get(client, path)


def main():
    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=dict(
            arguments.get_spec("auth", "name"),
            state=dict(
                default='enabled',
                choices=['enabled', 'disabled'],
            ),
            password=dict(
                no_log=True
            ),
            groups=dict(
                type='list', elements='str',
            )
        ),
    )

    client = arguments.get_sensu_client(module.params['auth'])
    path = utils.build_core_v2_path(None, 'users', module.params['name'])

    try:
        remote_object = utils.get(client, path)
    except errors.Error as e:
        module.fail_json(msg=str(e))

    if remote_object is None and module.params['password'] is None:
        module.fail_json(msg='Cannot create new user without a password')

    payload = arguments.get_spec_payload(module.params, 'password', 'groups')
    payload['username'] = module.params['name']
    payload['disabled'] = module.params['state'] == 'disabled'

    try:
        changed, user = sync(
            remote_object, client, path, payload, module.check_mode
        )
        module.exit_json(changed=changed, object=user)
    except errors.Error as e:
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    main()
