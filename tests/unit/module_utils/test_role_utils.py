# -*- coding: utf-8 -*-
# Copyright: (c) 2019, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible_collections.sensu.sensu_go.plugins.module_utils import role_utils


class TestDoSubjectsDiffer:
    def test_different_lengths(self):
        assert role_utils._do_subjects_differ(
            [{"type": "a", "name": "a"}],
            [{"type": "a", "name": "a"}, {"type": "a", "name": "b"}]
        ) is True

    def test_different_type_with_same_name(self):
        assert role_utils._do_subjects_differ(
            [{"type": "a", "name": "same"}],
            [{"type": "b", "name": "same"}]
        ) is True

    def test_equal_with_different_order_within_type(self):
        assert role_utils._do_subjects_differ(
            [{"type": "a", "name": "a2"}, {"type": "a", "name": "a1"}],
            [{"type": "a", "name": "a1"}, {"type": "a", "name": "a2"}]
        ) is False

    def test_equal_with_different_order_multiple_types(self):
        assert role_utils._do_subjects_differ(
            [
                {"type": "a", "name": "a2"},
                {"type": "b", "name": "b1"},
                {"type": "a", "name": "a1"}
            ],
            [
                {"type": "a", "name": "a1"},
                {"type": "a", "name": "a2"},
                {"type": "b", "name": "b1"}
            ]
        ) is False

    def test_different(self):
        assert role_utils._do_subjects_differ(
            [
                {"type": "a", "name": "a2"},
                {"type": "b", "name": "b3"},
            ],
            [
                {"type": "c", "name": "c2"},
                {"type": "a", "name": "s2"},
            ]
        ) is True


class TestDoDiffer:
    def test_new_role_binding(self):
        current = None
        desired = {
            'role_ref': 'a',
            'subjects': [
                {"type": "User", "name": "b"},
                {"type": "Group", "name": "g"},
            ]
        }
        assert role_utils.do_role_bindings_differ(current, desired) is True

    def test_equal_role_binding(self):
        current = {
            'role_ref': 'a',
            'subjects': [
                {"type": "User", "name": "b"},
                {"type": "Group", "name": "g"},
            ]
        }
        desired = {
            'role_ref': 'a',
            'subjects': [
                {"type": "User", "name": "b"},
                {"type": "Group", "name": "g"},
            ]
        }
        assert role_utils.do_role_bindings_differ(current, desired) is False

    def test_equal_role_binding_mixed_users_and_groups(self):
        current = {
            'role_ref': 'a',
            'subjects': [
                {"type": "Group", "name": "g1"},
                {"type": "User", "name": "u1"},
                {"type": "Group", "name": "g2"},
                {"type": "User", "name": "u2"},
            ]
        }
        desired = {
            'role_ref': 'a',
            'subjects': [
                {"type": "User", "name": "u2"},
                {"type": "User", "name": "u1"},
                {"type": "Group", "name": "g2"},
                {"type": "Group", "name": "g1"},
            ]
        }
        assert role_utils.do_role_bindings_differ(current, desired) is False

    def test_updated_role_binding_subjects(self):
        current = {
            'role_ref': 'a',
            'subjects': [
                {"type": "User", "name": "b"},
            ]
        }
        desired = {
            'role_ref': 'a',
            'subjects': [
                {"type": "User", "name": "b"},
                {"type": "Group", "name": "g"},
            ]
        }
        assert role_utils.do_role_bindings_differ(current, desired) is True
