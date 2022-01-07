from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import bonsai, errors
from ansible_collections.sensu.sensu_go.plugins.modules import bonsai_asset

from .common.utils import (
    AnsibleExitJson, AnsibleFailJson, ModuleTestCase, set_module_args,
)

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestBonsaiAsset(ModuleTestCase):
    def test_success(self, mocker):
        bonsai_params = mocker.patch.object(bonsai, "get_asset_parameters")
        bonsai_params.return_value = dict(sample="value")

        set_module_args(name="name", version="version")

        with pytest.raises(AnsibleExitJson):
            bonsai_asset.main()

    def test_bonsai_failure(self, mocker):
        bonsai_params = mocker.patch.object(bonsai, "get_asset_parameters")
        bonsai_params.side_effect = errors.BonsaiError("Bonsai bad")

        set_module_args(name="name", version="version")

        with pytest.raises(AnsibleFailJson):
            bonsai_asset.main()

    def test_validation_failure(self, mocker):
        bonsai_params = mocker.patch.object(bonsai, "get_asset_parameters")
        bonsai_params.return_value = dict(sample="value")

        set_module_args(version="version")

        with pytest.raises(AnsibleFailJson):
            bonsai_asset.main()
