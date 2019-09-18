from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, utils,
)
from ansible_collections.sensu.sensu_go.plugins.modules import asset

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)


class TestAsset(ModuleTestCase):
    def test_minimal_asset_parameters(self, mocker):
        sync_mock = mocker.patch.object(utils, "sync")
        sync_mock.return_value = True, {}
        set_module_args(
            name="test_asset",
            url="http://example.com/asset.tar.gz",
            sha512="sha512String",
        )

        with pytest.raises(AnsibleExitJson):
            asset.main()

        state, _client, path, payload, check_mode = sync_mock.call_args[0]
        assert state == "present"
        assert path == "/assets/test_asset"
        assert payload == dict(
            url="http://example.com/asset.tar.gz",
            sha512="sha512String",
            metadata=dict(
                name="test_asset",
                namespace="default",
            ),
        )
        assert check_mode is False

    def test_all_asset_parameters(self, mocker):
        sync_mock = mocker.patch.object(utils, "sync")
        sync_mock.return_value = True, {}
        set_module_args(
            name="test_asset",
            state="absent",
            url="http://example.com/asset.tar.gz",
            sha512="sha512String",
            filters=["a", "b", "c"],
            headers={"header": "h"},
            labels={"region": "us-west-1"},
            annotations={"playbook": 12345},
        )

        with pytest.raises(AnsibleExitJson):
            asset.main()

        state, _client, path, payload, check_mode = sync_mock.call_args[0]
        assert state == "absent"
        assert path == "/assets/test_asset"
        assert payload == dict(
            url="http://example.com/asset.tar.gz",
            sha512="sha512String",
            filters=["a", "b", "c"],
            headers={"header": "h"},
            metadata=dict(
                name="test_asset",
                namespace="default",
                labels={"region": "us-west-1"},
                annotations={"playbook": "12345"},
            ),
        )
        assert check_mode is False

    def test_failure(self, mocker):
        sync_mock = mocker.patch.object(utils, "sync")
        sync_mock.side_effect = errors.Error("Bad error")
        set_module_args(
            name="test_asset",
            url="http://example.com/asset.tar.gz",
            sha512="sha512String",
        )

        with pytest.raises(AnsibleFailJson):
            asset.main()
