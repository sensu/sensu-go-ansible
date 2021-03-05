from __future__ import absolute_import, division, print_function
__metaclass__ = type

import sys

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, utils,
)
from ansible_collections.sensu.sensu_go.plugins.modules import namespace

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestNamespace(ModuleTestCase):
    def test_namespace(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.return_value = True, {}
        set_module_args(
            name='dev'
        )

        with pytest.raises(AnsibleExitJson):
            namespace.main()

        state, _client, path, payload, check_mode = sync_mock.call_args[0]
        assert state == 'present'
        assert path == '/api/core/v2/namespaces/dev'
        assert payload == dict(
            name='dev'
        )
        assert check_mode is False

    def test_failure(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.side_effect = errors.Error('Bad error')
        set_module_args(
            name='dev',
        )

        with pytest.raises(AnsibleFailJson):
            namespace.main()
