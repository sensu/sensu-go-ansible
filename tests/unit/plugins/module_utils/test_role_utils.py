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


class TestDoRoleBindingsDiffer:
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


class TestRuleSets:
    def test_all_keys_none(self):
        assert role_utils._rule_set([{}]) == {
            (frozenset(), frozenset(), frozenset())
        }

    def test_rules_multiple(self):
        assert role_utils._rule_set([{
            'verbs': ['list', 'get'],
            'resources': ['entities', 'checks'],
            'resource_names': None
        }, {
            'verbs': ['list', 'delete'],
            'resources': ['entities', 'checks'],
            'resource_names': None
        }]) == {
            (frozenset(['delete', 'list']), frozenset(['checks', 'entities']), frozenset()),
            (frozenset(['get', 'list']), frozenset(['checks', 'entities']), frozenset())
        }

    def test_missing_key(self):
        assert role_utils._rule_set([{
            'verbs': ['list', 'get'],
            'resources': ['entities', 'checks'],
        }]) == {
            (frozenset(['get', 'list']), frozenset(['checks', 'entities']), frozenset())
        }


class TestDoRulesDiffer:
    def test_empty_values(self):
        assert role_utils._do_rules_differ(
            [{'verbs': []}],
            [{'verbs': []}]
        ) is False

    def test_rules_when_current_values_are_none(self):
        assert role_utils._do_rules_differ(
            [{'verbs': None}],
            [{'verbs': ['get', 'list']}]
        ) is True

    def test_rules_when_desired_values_are_none(self):
        assert role_utils._do_rules_differ(
            [{'verbs': ['get', 'list']}],
            [{'verbs': None}]
        ) is True

    def test_rules_are_different(self):
        assert role_utils._do_rules_differ(
            [{'verbs': ['list', 'get']}],
            [{'verbs': ['get', 'delete']}]
        ) is True

    def test_rules_with_additional_keys_in_current(self):
        assert role_utils._do_rules_differ(
            [{'verbs': ['list', 'get'], 'resources': ['checks', 'entities']}],
            [{'verbs': ['get', 'list']}]
        ) is True

    def test_rules_are_the_same(self):
        assert role_utils._do_rules_differ(
            [{'verbs': ['list', 'get']}],
            [{'verbs': ['get', 'list']}]
        ) is False


class TestDoRolesDiffer:
    def test_rules_when_values_in_current_are_none(self):
        current = {
            'rules': [{
                'resource_names': None
            }]
        }
        desired = {
            'rules': [{
                'resource_names': ['check-cpu']
            }]
        }
        assert role_utils.do_roles_differ(current, desired) is True

    def test_rules_when_values_in_desired_are_none(self):
        current = {
            'rules': [{
                'resource_names': ['check-cpu']
            }]
        }
        desired = {
            'rules': [{
                'resource_names': None
            }]
        }
        assert role_utils.do_roles_differ(current, desired) is True

    def test_different_rules_order(self):
        current = {
            'rules': [{
                'verbs': ['get', 'list'],
                'resources': ['entities', 'checks']
            }, {
                'verbs': ['create', 'delete', 'update'],
                'resources': ['assets', 'hooks']
            }]
        }
        desired = {
            'rules': [{
                'verbs': ['delete', 'create', 'update'],
                'resources': ['hooks', 'assets']
            }, {
                'verbs': ['list', 'get'],
                'resources': ['checks', 'entities']
            }]
        }
        assert role_utils.do_roles_differ(current, desired) is False

    def test_key_missing_in_current(self):
        current = {
            'rules': [{
                'verbs': ['update', 'create'],
                'resources': ['hooks', 'assets']
            }]
        }
        desired = {
            'rules': [{
                'verbs': ['create', 'update'],
                'resources': ['hooks', 'assets'],
                'resource_names': ['check-cpu']
            }]
        }
        assert role_utils.do_roles_differ(current, desired) is True

    def test_key_missing_in_desired(self):
        current = {
            'rules': [{
                'verbs': ['update', 'create'],
                'resources': ['hooks', 'assets'],
                'resource_names': ['check-cpu']
            }]
        }
        desired = {
            'rules': [{
                'verbs': ['create', 'update'],
                'resources': ['hooks', 'assets']
            }]
        }
        assert role_utils.do_roles_differ(current, desired) is True

    def test_role_exists_but_with_additional_rules(self):
        current = {
            'rules': [{
                'verbs': ['get', 'list'],
                'resources': ['entities', 'check']
            }, {
                'verbs': ['create', 'update', 'delete'],
                'resources': ['assets', 'hooks']
            }]
        }
        desired = {
            'rules': [{
                'verbs': ['list', 'get'],
                'resources': ['check', 'entities']
            }]
        }
        assert role_utils.do_roles_differ(current, desired) is True
