# -*- coding: utf-8 -*-
# Copyright: (c) 2019, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


def type_name_dict(obj_type, name):
    return {
        'type': obj_type,
        'name': name,
    }


def build_subjects(groups, users):
    groups_dicts = [type_name_dict('Group', g) for g in (groups or [])]
    users_dicts = [type_name_dict('User', u) for u in (users or [])]

    return groups_dicts + users_dicts


def do_role_bindings_differ(current, desired):
    if current is None:
        return True

    for key, value in desired.items():
        current_value = current.get(key)
        if key == 'subjects':
            if _do_subjects_differ(current_value, value):
                return True
        elif value != current_value:
            return True

    return False


# sorts a list of subjects (dicts returned by type_name_dict)
# by 'type' and 'name' keys and returns the result of comparison.
def _do_subjects_differ(a, b):
    sorted_a = sorted(a, key=lambda x: (x['type'], x['name']))
    sorted_b = sorted(b, key=lambda x: (x['type'], x['name']))
    return sorted_a != sorted_b
