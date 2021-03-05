from __future__ import absolute_import, division, print_function
__metaclass__ = type

import sys

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, utils,
)
from ansible_collections.sensu.sensu_go.plugins.modules import silence

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestSilence(ModuleTestCase):
    def test_minimal_silence_parameters_check(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.return_value = True, {}
        set_module_args(
            check='check'
        )

        with pytest.raises(AnsibleExitJson):
            silence.main()

        state, _client, path, payload, check_mode = sync_mock.call_args[0]
        assert state == 'present'
        assert path == '/api/core/v2/namespaces/default/silenced/%2A%3Acheck'  # %2A = *, %3A = :
        assert payload == dict(
            check='check',
            metadata=dict(
                name='*:check',
                namespace='default',
            ),
        )
        assert check_mode is False

    def test_minimal_silence_parameters_subscription(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.return_value = True, {}
        set_module_args(
            subscription='subscription'
        )

        with pytest.raises(AnsibleExitJson):
            silence.main()

        state, _client, path, payload, check_mode = sync_mock.call_args[0]
        assert state == 'present'
        assert path == '/api/core/v2/namespaces/default/silenced/subscription%3A%2A'  # %3A = :, %2A = *
        assert payload == dict(
            subscription='subscription',
            metadata=dict(
                name='subscription:*',
                namespace='default',
            ),
        )
        assert check_mode is False

    def test_all_silence_parameters(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.return_value = True, {}
        set_module_args(
            namespace='my',
            subscription='entity:test-entity',
            check='check',
            state='absent',
            begin=1542671205,
            expire=1542771205,
            expire_on_resolve=True,
            reason='because',
            labels={'region': 'us-west-1'},
            annotations={'playbook': 12345},
        )

        with pytest.raises(AnsibleExitJson):
            silence.main()

        state, _client, path, payload, check_mode = sync_mock.call_args[0]
        assert state == 'absent'
        assert path == '/api/core/v2/namespaces/my/silenced/entity%3Atest-entity%3Acheck'  # %3A = :
        assert payload == dict(
            subscription='entity:test-entity',
            check='check',
            begin=1542671205,
            expire=1542771205,
            expire_on_resolve=True,
            reason='because',
            metadata=dict(
                name='entity:test-entity:check',
                namespace='my',
                labels={'region': 'us-west-1'},
                annotations={'playbook': '12345'},
            ),
        )
        assert check_mode is False

    def test_failure_when_both_params_are_missing(self):
        set_module_args()

        with pytest.raises(AnsibleFailJson,
                           match='one of the following is required: subscription, check'):
            silence.main()

    def test_failure(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.side_effect = errors.Error('Bad error')
        set_module_args(
            subscription='subscription'
        )

        with pytest.raises(AnsibleFailJson):
            silence.main()
