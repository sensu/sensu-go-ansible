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


class TestDoDiffer:
    def test_equal_assets_with_none_values(self):
        assert asset.do_differ(
            {
                "name": "asset",
                "builds": [
                    {
                        "sha512": "a",
                        "url": "a",
                        "filters": None
                    },
                ],
            },
            {
                "name": "asset",
                "builds": [
                    {
                        "sha512": "a",
                        "url": "a",
                        "headers": None,
                    },
                ],
            },
        ) is False

    def test_equal_assets_with_different_build_content(self):
        assert asset.do_differ(
            {
                "name": "asset",
                "builds": [
                    {
                        "url": "http://abc.com",
                        "sha512": "abc",
                        "headers": {
                            "foo": "bar",
                            "bar": "foo",
                        }
                    },
                    {
                        "url": "http://def.com",
                        "sha512": "def",
                        "filters": ["d == d", "e == e"],
                    },

                ]
            },
            {
                "name": "asset",
                "builds": [
                    {
                        "url": "http://def.com",
                        "sha512": "def",
                        "filters": ["e == e", "d == d"],
                    },
                    {
                        "url": "http://abc.com",
                        "sha512": "abc",
                        "headers": {
                            "bar": "foo",
                            "foo": "bar"
                        }
                    },
                ]
            },
        ) is False

    def test_updated_asset(self):
        assert asset.do_differ(
            {
                "name": "asset",
                "builds": [
                    {
                        "url": "http://abc.com",
                        "sha512": "abc",
                    }
                ],
                "annotations": {
                    "foo": "bar",
                }
            },
            {
                "name": "asset",
                "builds": [
                    {
                        "url": "http://def.com",
                        "sha512": "abc",
                    },
                    {
                        "url": "http://def.com",
                        "sha512": "abc",
                        "filters": ["abc == def"],
                    }
                ],
            },
        ) is True

    def test_different_assets_with_same_builds(self):
        assert asset.do_differ(
            {
                "name": "a",
                "builds": [
                    {
                        "url": "http://abc.com",
                        "sha512": "abc",
                    }
                ],
                "annotations": {
                    "foo": "bar",
                }
            },
            {
                "name": "b",
                "builds": [
                    {
                        "url": "http://abc.com",
                        "sha512": "abc",
                    }
                ],
                "annotations": {
                    "bar": "foo"
                }
            },
        ) is True


class TestAsset(ModuleTestCase):
    def test_minimal_asset_parameters(self, mocker):
        sync_mock = mocker.patch.object(utils, "sync")
        sync_mock.return_value = True, {}
        set_module_args(
            name="test_asset",
            builds=[
                dict(
                    url="http://example.com/asset.tar.gz",
                    sha512="sha512String",
                ),
            ]
        )

        with pytest.raises(AnsibleExitJson):
            asset.main()

        state, _client, path, payload, check_mode, _do_differ = sync_mock.call_args[0]
        assert state == "present"
        assert path == "/api/core/v2/namespaces/default/assets/test_asset"
        assert payload == dict(
            builds=[
                dict(
                    url="http://example.com/asset.tar.gz",
                    sha512="sha512String",
                ),
            ],
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
            namespace="my",
            state="present",
            builds=[
                dict(
                    url="http://example.com/asset.tar.gz",
                    sha512="sha512String",
                    filters=["a", "b", "c"],
                    headers={"header": "h"},
                ),
            ],
            labels={"region": "us-west-1"},
            annotations={"playbook": 12345},
        )

        with pytest.raises(AnsibleExitJson):
            asset.main()

        state, _client, path, payload, check_mode, _do_differ = sync_mock.call_args[0]
        assert state == "present"
        assert path == "/api/core/v2/namespaces/my/assets/test_asset"
        assert payload == dict(
            builds=[
                dict(
                    url="http://example.com/asset.tar.gz",
                    sha512="sha512String",
                    filters=["a", "b", "c"],
                    headers={"header": "h"},
                )
            ],
            metadata=dict(
                name="test_asset",
                namespace="my",
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
            builds=[
                dict(
                    url="http://example.com/asset.tar.gz",
                    sha512="sha512String",
                )
            ]

        )

        with pytest.raises(AnsibleFailJson):
            asset.main()

    def test_failure_empty_builds(self, mocker):
        sync_mock = mocker.patch.object(utils, 'sync')
        sync_mock.side_effect = Exception("Validation should fail but didn't")
        set_module_args(
            name="test_asset",
            builds=[],
        )

        with pytest.raises(AnsibleFailJson):
            asset.main()
