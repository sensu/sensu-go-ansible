# -*- coding: utf-8 -*-
# Copyright: (c) 2019, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible_collections.sensu.sensu_go.plugins.module_utils import errors, debug
from ansible.module_utils.six import string_types


def sync(state, client, path, payload, check_mode):
    remote_object = get(client, path)

    if state == "absent" and remote_object is None:
        return False, None

    if state == "absent":
        if not check_mode:
            delete(client, path)
        return True, None

    # Making sure remote_object is present from here on

    if do_differ(remote_object, payload):
        if check_mode:
            return True, payload
        put(client, path, payload)
        return True, get(client, path)

    return False, remote_object


def _is_same_type(a, b):
    if isinstance(a, string_types) and isinstance(b, string_types):
        return True
    elif a is None or b is None:
        # It means that one or both values are empty, could still be same type
        return True
    return isinstance(a, type(b))


def do_differ(current, desired):
    if current is None:
        return True
    for key, value in desired.items():
        current_value = current.get(key)
        if not _is_same_type(current_value, value):
            debug.log("Remote and local value on key '{0}' structurally mismatch", key)
            return True
        elif isinstance(value, dict):
            if do_differ(current_value, value):
                return True
        elif value != current_value:
            return True

    return False


def _abort(msg, *args, **kwargs):
    raise errors.SyncError(msg.format(*args, **kwargs))


def get(client, path):
    resp = client.get(path)
    if resp.status not in (200, 404):
        _abort(
            "GET {0} failed with status {1}: {2}", path, resp.status, resp.data,
        )
    if resp.status == 200 and resp.json is None:
        _abort("Server returned invalid JSON {0}", resp.data)
    return resp.json


def delete(client, path):
    resp = client.delete(path)
    if resp.status != 204:
        _abort(
            "DELETE {0} failed with status {1}: {2}",
            path, resp.status, resp.data,
        )
    return None


def put(client, path, payload):
    resp = client.put(path, payload)
    if resp.status != 201:
        _abort(
            "PUT {0} failed with status {1}: {2}",
            path, resp.status, resp.data,
        )
    return None


def dict_to_single_item_dicts(data):
    return [{k: v} for k, v in data.items()]


def dict_to_key_value_strings(data):
    return ["{0}={1}".format(k, v) for k, v in data.items()]
