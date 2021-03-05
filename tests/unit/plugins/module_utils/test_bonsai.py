# -*- coding: utf-8 -*-
# Copyright: (c) 2019, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import sys

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    bonsai, errors, http,
)

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestGet:
    def test_url_construction(self, mocker):
        http_mock = mocker.patch.object(bonsai, "http")
        http_mock.request.return_value = http.Response(200, "{}")

        bonsai.get("path")

        assert http_mock.request.call_args[0] == (
            "GET", "https://bonsai.sensu.io/api/v1/assets/path",
        )

    def test_bad_status(self, mocker):
        http_mock = mocker.patch.object(bonsai, "http")
        http_mock.request.return_value = http.Response(400, "{}")

        with pytest.raises(errors.BonsaiError, match="400"):
            bonsai.get("path")

    def test_invalid_json(self, mocker):
        http_mock = mocker.patch.object(bonsai, "http")
        http_mock.request.return_value = http.Response(200, "{ a }")

        with pytest.raises(errors.BonsaiError, match="JSON"):
            bonsai.get("path")


class TestGetAvailableAssetVersions:
    def test_valid_data(self, mocker):
        get = mocker.patch.object(bonsai, "get")
        get.return_value = dict(
            versions=[
                dict(version="1.2.3", assets=[]),
                dict(version="1.2.4", assets=[]),
                dict(version="1.2.5", assets=[]),
            ],
        )

        result = bonsai.get_available_asset_versions("namespace", "name")

        assert set(("1.2.3", "1.2.4", "1.2.5")) == result
        assert get.call_args[0] == ("namespace/name",)

    @pytest.mark.parametrize("data", [
        "invalid",
        dict(invalid="toplevel"),
        dict(versions="oh-no"),
        dict(versions=["not", "ok"]),
        dict(versions=[dict(invalid="internal")]),
    ])
    def test_invalid_data(self, mocker, data):
        get = mocker.patch.object(bonsai, "get")
        get.return_value = data

        with pytest.raises(errors.BonsaiError, match="versions"):
            bonsai.get_available_asset_versions("namespace", "name")


class TestGetAssetVersionBuilds:
    def test_url_construction(self, mocker):
        get = mocker.patch.object(bonsai, "get")
        get.return_value = dict(spec=dict(builds=[]))

        bonsai.get_asset_version_builds("x", "y", "z")

        assert get.call_args[0] == ("x/y/z/release_asset_builds",)

    @pytest.mark.parametrize("data", [
        "invalid",
        dict(missing="spec"),
        dict(spec="invalid"),
        dict(spec=dict(missing="builds")),
    ])
    def test_invalid_data(self, mocker, data):
        get = mocker.patch.object(bonsai, "get")
        get.return_value = data

        with pytest.raises(errors.BonsaiError, match="spec"):
            bonsai.get_asset_version_builds("x", "y", "z")


class TestGetAssetParameters:
    def test_valid_all_data(self, mocker):
        versions = mocker.patch.object(bonsai, "get_available_asset_versions")
        versions.return_value = set(("t", "u", "v"))
        builds = mocker.patch.object(bonsai, "get_asset_version_builds")
        builds.return_value = dict(
            metadata=dict(
                annotations=dict(annotation="value"),
                labels=dict(label="value"),
            ),
            spec=dict(builds=[1, 2, 3]),
        )

        result = bonsai.get_asset_parameters("x/y", "v")

        assert result == dict(
            labels=dict(label="value"),
            annotations=dict(annotation="value"),
            builds=[1, 2, 3],
        )
        assert versions.call_args[0] == ("x", "y")
        assert builds.call_args[0] == ("x", "y", "v")

    def test_valid_minimal_data(self, mocker):
        versions = mocker.patch.object(bonsai, "get_available_asset_versions")
        versions.return_value = set(("t", "u", "v"))
        builds = mocker.patch.object(bonsai, "get_asset_version_builds")
        builds.return_value = dict(
            spec=dict(builds=[1, 2, 3]),
        )

        result = bonsai.get_asset_parameters("x/y", "v")

        assert result == dict(
            labels=None,
            annotations=None,
            builds=[1, 2, 3],
        )
        assert versions.call_args[0] == ("x", "y")
        assert builds.call_args[0] == ("x", "y", "v")

    def test_invalid_name(self, mocker):
        with pytest.raises(errors.BonsaiError, match="names"):
            bonsai.get_asset_parameters("x.y", "v")

    def test_invalid_version(self, mocker):
        versions = mocker.patch.object(bonsai, "get_available_asset_versions")
        versions.return_value = set(("t", "u"))

        with pytest.raises(errors.BonsaiError, match="Version"):
            bonsai.get_asset_parameters("x/y", "v")
