from __future__ import absolute_import, division, print_function
__metaclass__ = type

import sys

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, utils,
)
from ansible_collections.sensu.sensu_go.plugins.modules import cluster

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestCluster(ModuleTestCase):
    @pytest.mark.parametrize("params", [
        {"name": "demo", "state": "absent"},
        {"name": "demo", "api_urls": "url"},
    ])
    def test_minimal_parameters(self, mocker, params):
        mocker.patch.object(utils, "sync_v1").return_value = True, {}
        set_module_args(**params)

        with pytest.raises(AnsibleExitJson):
            cluster.main()

    def test_all_parameters(self, mocker):
        sync_mock = mocker.patch.object(utils, "sync_v1")
        sync_mock.return_value = True, {}
        set_module_args(
            auth=dict(
                user="user",
                password="pass",
                url="http://127.0.0.1:1234",
                api_key="123-key",
                verify=False,
                ca_path="/tmp/ca.bundle",
            ),
            state="present",
            name="demo",
            api_urls=["a", "b"],
        )

        with pytest.raises(AnsibleExitJson):
            cluster.main()

        state, _client, path, payload, check_mode = sync_mock.call_args[0]
        assert state == "present"
        assert path == "/api/enterprise/federation/v1/clusters/demo"
        assert payload == dict(
            type="Cluster",
            api_version="federation/v1",
            metadata=dict(name="demo"),
            spec=dict(api_urls=["a", "b"]),
        )
        assert check_mode is False

    @pytest.mark.parametrize("skip", ["api_urls"])
    def test_missing_required_param_present(self, mocker, skip):
        sync_mock = mocker.patch.object(utils, "sync_v1")
        all_args = dict(name="demo", api_urls="url")
        set_module_args(**dict((k, v) for k, v in all_args.items() if k != skip))

        with pytest.raises(AnsibleFailJson):
            cluster.main()

        sync_mock.assert_not_called()

    def test_failure(self, mocker):
        mocker.patch.object(utils, "sync_v1").side_effect = (
            errors.Error("Bad error")
        )
        set_module_args(name="demo", state="absent")

        with pytest.raises(AnsibleFailJson):
            cluster.main()
