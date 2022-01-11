from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys

import pytest

from ansible.playbook.task import Task

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    bonsai, errors,
)
from ansible_collections.sensu.sensu_go.plugins.action import bonsai_asset

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestValidate:
    @pytest.mark.parametrize("name,args,required,typ", [
        # Required values must match the selected type.
        ("a", dict(a=3), True, int),
        ("a", dict(a=3.3), True, float),
        ("a", dict(a="b"), True, str),
        ("a", dict(a=[]), True, list),
        ("a", dict(a={}), True, dict),
        # Optional values are not checked for type-correctness if they are
        # missing.
        ("a", dict(), False, int),
        ("a", dict(), False, float),
        ("a", dict(), False, str),
        ("a", dict(), False, list),
        ("a", dict(), False, dict),
    ])
    def test_valid_values(self, name, args, required, typ):
        bonsai_asset.validate(name, args, required, typ)

    def test_missing_required(self):
        with pytest.raises(errors.Error, match="required"):
            bonsai_asset.validate("a", {}, True, str)

    def test_invalid_type(self):
        with pytest.raises(errors.Error, match="should"):
            bonsai_asset.validate("a", dict(a=3), True, str)

    def test_invalid_type_for_optional_value(self):
        with pytest.raises(errors.Error, match="should"):
            bonsai_asset.validate("a", dict(a=3), False, dict)


class TestValidateArguments:
    def test_valid_minimal_args(self):
        bonsai_asset.ActionModule.validate_arguments(dict(
            name="abc", version="1.2.3",
        ))

    def test_valid_all_args(self):
        bonsai_asset.ActionModule.validate_arguments(dict(
            name="abc", version="1.2.3", rename="def",
            labels={}, annotations={},
        ))

    def test_valid_unicode_strings_python2(self):
        bonsai_asset.ActionModule.validate_arguments(dict(
            name=u"abc", version=u"1.2.3", rename=u"def",
            labels={}, annotations={},
        ))

    def test_invalid_name(self):
        with pytest.raises(errors.Error, match="name"):
            bonsai_asset.ActionModule.validate_arguments(dict(
                name=1.234, version="1.2.3",
            ))

    def test_missing_name(self):
        with pytest.raises(errors.Error, match="name"):
            bonsai_asset.ActionModule.validate_arguments(dict(
                version="1.2.3",
            ))

    def test_invalid_version(self):
        with pytest.raises(errors.Error, match="version"):
            bonsai_asset.ActionModule.validate_arguments(dict(
                name="abc", version=1.2,
            ))

    def test_missing_version(self):
        with pytest.raises(errors.Error, match="version"):
            bonsai_asset.ActionModule.validate_arguments(dict(
                name="abc",
            ))

    def test_invalid_rename(self):
        with pytest.raises(errors.Error, match="rename"):
            bonsai_asset.ActionModule.validate_arguments(dict(
                name="abc", version="1.2.3", rename=1,
            ))

    def test_invalid_labels(self):
        with pytest.raises(errors.Error, match="labels"):
            bonsai_asset.ActionModule.validate_arguments(dict(
                name="abc", version="1.2.3", labels=1,
            ))

    def test_invalid_annotations(self):
        with pytest.raises(errors.Error, match="annotations"):
            bonsai_asset.ActionModule.validate_arguments(dict(
                name="abc", version="1.2.3", annotations=1,
            ))


class TestBuildAssetArgs:
    def test_no_additional_metadata(self):
        result = bonsai_asset.ActionModule.build_asset_args(
            dict(name="test/asset", version="1.2.3"),
            dict(builds=[], labels=None, annotations=None),
        )

        assert result == dict(
            name="test/asset",
            state="present",
            builds=[],
        )

    def test_bonsai_metadata_only(self):
        result = bonsai_asset.ActionModule.build_asset_args(
            dict(name="test/asset", version="1.2.3"),
            dict(builds=[], labels=dict(a="b"), annotations=dict(c="d")),
        )

        assert result == dict(
            name="test/asset",
            state="present",
            builds=[],
            annotations=dict(c="d"),
            labels=dict(a="b"),
        )

    def test_user_metadata_only(self):
        result = bonsai_asset.ActionModule.build_asset_args(
            dict(
                name="test/asset",
                version="1.2.3",
                labels=dict(my="label"),
                annotations=dict(my="annotation"),
            ),
            dict(builds=[1, 2, 3], labels=None, annotations=None),
        )

        assert result == dict(
            name="test/asset",
            state="present",
            builds=[1, 2, 3],
            annotations=dict(my="annotation"),
            labels=dict(my="label"),
        )

    def test_mixed_metadata(self):
        result = bonsai_asset.ActionModule.build_asset_args(
            dict(
                name="test/asset",
                version="1.2.3",
                labels=dict(my="label"),
                annotations=dict(my="annotation"),
            ),
            dict(builds=[], labels=dict(my="x", a="b"), annotations=dict(my="c")),
        )

        assert result == dict(
            name="test/asset",
            state="present",
            builds=[],
            annotations=dict(my="annotation"),
            labels=dict(my="label", a="b"),
        )

    def test_rename(self):
        result = bonsai_asset.ActionModule.build_asset_args(
            dict(name="test/asset", version="1.2.3", rename="my-asset"),
            dict(builds=[], labels=None, annotations=None),
        )

        assert result == dict(
            name="my-asset",
            state="present",
            builds=[],
        )

    def test_auth_passthrough(self):
        result = bonsai_asset.ActionModule.build_asset_args(
            dict(
                auth=dict(url="http://localhost:1234"),
                name="test/asset",
                version="1.2.3",
            ),
            dict(builds=[], labels=None, annotations=None),
        )

        assert result == dict(
            auth=dict(url="http://localhost:1234"),
            name="test/asset",
            state="present",
            builds=[],
        )

    def test_namespace_passthrough(self):
        result = bonsai_asset.ActionModule.build_asset_args(
            dict(namespace='default', name="test/asset", version="1.2.3"),
            dict(builds=[], labels=None, annotations=None),
        )

        assert result == dict(
            name="test/asset",
            namespace='default',
            state="present",
            builds=[],
        )


class TestDownloadAssetDefinition:
    def get_mock_action(self, mocker, result):
        action = bonsai_asset.ActionModule(
            mocker.MagicMock(), mocker.MagicMock(), mocker.MagicMock(), loader=None,
            templar=None, shared_loader_obj=None,
        )
        action._execute_module = mocker.MagicMock(return_value=result)
        return action

    def test_download_on_control_node(self, mocker):
        bonsai_params = mocker.patch.object(bonsai, "get_asset_parameters")
        bonsai_params.return_value = dict(sample="value")
        action = self.get_mock_action(mocker, {})

        result = action.download_asset_definition(
            on_remote=False, name="test/asset", version="1.2.3", task_vars=None,
        )

        assert result == dict(sample="value")
        bonsai_params.assert_called_once()
        action._execute_module.assert_not_called()

    def test_fail_download_on_control_node(self, mocker):
        bonsai_params = mocker.patch.object(bonsai, "get_asset_parameters")
        bonsai_params.side_effect = errors.BonsaiError("Bonsai bad")
        action = self.get_mock_action(mocker, {})

        with pytest.raises(errors.Error, match="Bonsai bad"):
            action.download_asset_definition(
                on_remote=False, name="test/asset", version="1.2.3", task_vars=None,
            )

        bonsai_params.assert_called_once()
        action._execute_module.assert_not_called()

    def test_download_on_target_node(self, mocker):
        bonsai_params = mocker.patch.object(bonsai, "get_asset_parameters")
        action = self.get_mock_action(mocker, dict(asset="sample"))

        result = action.download_asset_definition(
            on_remote=True, name="test/asset", version="1.2.3", task_vars=None,
        )

        assert result == "sample"
        bonsai_params.assert_not_called()
        action._execute_module.assert_called_once()

    def test_fail_on_target_node(self, mocker):
        bonsai_params = mocker.patch.object(bonsai, "get_asset_parameters")
        action = self.get_mock_action(mocker, dict(failed=True, msg="Bad err"))

        with pytest.raises(errors.Error, match="Bad err"):
            action.download_asset_definition(
                on_remote=True, name="test/asset", version="1.2.3", task_vars=None,
            )

        bonsai_params.assert_not_called()
        action._execute_module.assert_called_once()


class TestRun:
    def test_success(self, mocker):
        task = mocker.MagicMock(Task, async_val=0, args=dict(
            name="test/asset",
            version="1.2.3",
        ))
        action = bonsai_asset.ActionModule(
            task, mocker.MagicMock(), mocker.MagicMock(), loader=None,
            templar=None, shared_loader_obj=None,
        )
        action._execute_module = mocker.MagicMock(return_value=dict(a=3))
        action.download_asset_definition = mocker.MagicMock(
            return_value=dict(builds=[], labels=None, annotations=None),
        )

        result = action.run()

        assert result == dict(a=3)

    def test_fail(self, mocker):
        task = mocker.MagicMock(Task, async_val=0, args=dict(
            name="test/asset",
        ))
        action = bonsai_asset.ActionModule(
            task, mocker.MagicMock(), mocker.MagicMock(), loader=None,
            templar=None, shared_loader_obj=None,
        )
        action._execute_module = mocker.MagicMock(return_value=dict(a=3))
        action.download_asset_definition = mocker.MagicMock(
            return_value=dict(builds=[], labels=None, annotations=None),
        )

        result = action.run()

        assert result["failed"] is True
