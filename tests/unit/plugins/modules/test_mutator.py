from __future__ import absolute_import, division, print_function
__metaclass__ = type

import sys

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, utils,
)
from ansible_collections.sensu.sensu_go.plugins.modules import mutator

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestDoDiffer:
    @pytest.mark.parametrize("current,desired", [
        (  # No diff in params, no secrets
            dict(name="demo"),
            dict(name="demo"),
        ),
        (  # No diff in params, no diff in secrets
            dict(name="demo", secrets=[
                dict(name="n1", secret="s1"), dict(name="n2", secret="s2"),
            ]),
            dict(name="demo", secrets=[
                dict(name="n2", secret="s2"), dict(name="n1", secret="s1"),
            ]),
        ),
    ])
    def test_no_difference(self, current, desired):
        assert mutator.do_differ(current, desired) is False

    @pytest.mark.parametrize("current,desired", [
        (  # Diff in params, no diff in secrets
            dict(name="demo", secrets=[dict(name="a", secret="1")]),
            dict(name="prod", secrets=[dict(name="a", secret="1")]),
        ),
        (  # No diff in params, missing and set secrets
            dict(name="demo", secrets=[dict(name="a", secret="1")]),
            dict(name="demo", secrets=[dict(name="b", secret="2")]),
        ),
        (  # Diff in params, missing and set secrets
            dict(name="demo", secrets=[dict(name="a", secret="1")]),
            dict(name="prod", secrets=[dict(name="b", secret="2")]),
        ),
    ])
    def test_difference(self, current, desired):
        assert mutator.do_differ(current, desired) is True


class TestMutator(ModuleTestCase):
    def test_minimal_mutator_parameters(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.return_value = True, {}
        set_module_args(
            name='test_mutator',
            command='/bin/true',
        )

        with pytest.raises(AnsibleExitJson):
            mutator.main()

        state, _client, path, payload, check_mode, _d = sync_mock.call_args[0]
        assert state == 'present'
        assert path == '/api/core/v2/namespaces/default/mutators/test_mutator'
        assert payload == dict(
            command='/bin/true',
            metadata=dict(
                name='test_mutator',
                namespace='default',
            ),
        )
        assert check_mode is False

    def test_all_mutator_parameters(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.return_value = True, {}
        set_module_args(
            name='test_mutator',
            namespace='my',
            state='absent',
            command='/bin/true',
            timeout=30,
            runtime_assets='awesomeness',
            labels={'region': 'us-west-1'},
            annotations={'playbook': 12345},
            secrets=[dict(name="a", secret="b")],
        )

        with pytest.raises(AnsibleExitJson):
            mutator.main()

        state, _client, path, payload, check_mode, _d = sync_mock.call_args[0]
        assert state == 'absent'
        assert path == '/api/core/v2/namespaces/my/mutators/test_mutator'
        assert payload == dict(
            command='/bin/true',
            timeout=30,
            runtime_assets=['awesomeness'],
            metadata=dict(
                name='test_mutator',
                namespace='my',
                labels={'region': 'us-west-1'},
                annotations={'playbook': '12345'},
            ),
            secrets=[dict(name="a", secret="b")],
        )
        assert check_mode is False

    def test_failure(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.side_effect = errors.Error('Bad error')
        set_module_args(
            name='test_mutator',
            command='/bion/true'
        )

        with pytest.raises(AnsibleFailJson):
            mutator.main()
