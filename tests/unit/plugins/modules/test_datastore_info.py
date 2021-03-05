from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, utils,
)
from ansible_collections.sensu.sensu_go.plugins.modules import datastore_info

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)


class TestDatastoreInfo(ModuleTestCase):
    def test_get_all_datastores(self, mocker):
        get_mock = mocker.patch.object(utils, "get")
        get_mock.return_value = [dict(spec=1), dict(spec=2)]
        set_module_args()

        with pytest.raises(AnsibleExitJson) as context:
            datastore_info.main()

        _client, path = get_mock.call_args[0]
        assert path == "/api/enterprise/store/v1/provider"
        assert context.value.args[0]["objects"] == [1, 2]

    def test_get_single_datastore(self, mocker):
        get_mock = mocker.patch.object(utils, "get")
        get_mock.return_value = dict(spec=4)
        set_module_args(name="sample-datastore")

        with pytest.raises(AnsibleExitJson) as context:
            datastore_info.main()

        _client, path = get_mock.call_args[0]
        assert path == "/api/enterprise/store/v1/provider/sample-datastore"
        assert context.value.args[0]["objects"] == [4]

    def test_missing_single_datastore(self, mocker):
        get_mock = mocker.patch.object(utils, "get")
        get_mock.return_value = None
        set_module_args(name="sample-datastore")

        with pytest.raises(AnsibleExitJson) as context:
            datastore_info.main()

        assert context.value.args[0]["objects"] == []

    def test_failure(self, mocker):
        get_mock = mocker.patch.object(utils, "get")
        get_mock.side_effect = errors.Error("Bad error")
        set_module_args(name="sample-datastore")

        with pytest.raises(AnsibleFailJson):
            datastore_info.main()
