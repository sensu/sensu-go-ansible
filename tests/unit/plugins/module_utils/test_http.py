# -*- coding: utf-8 -*-
# Copyright: (c) 2019, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import ssl

import pytest

from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, http,
)


class TestResponse:
    def test_with_valid_json(self):
        resp = http.Response(201, '{"some": ["json", "data", 3]}')

        assert 201 == resp.status
        assert '{"some": ["json", "data", 3]}' == resp.data
        assert {"some": ["json", "data", 3]} == resp.json

    def test_with_invalid_json(self):
        resp = http.Response(404, "")

        assert 404 == resp.status
        assert "" == resp.data
        assert resp.json is None


class TestRequest:
    def test_ok_request(self, mocker):
        data_resp = mocker.Mock()
        data_resp.read.return_value = "data"
        data_resp.getcode.return_value = 200
        open_url = mocker.patch.object(http, "open_url")
        open_url.return_value = data_resp

        resp = http.request("GET", "example.com/path")

        assert 200 == resp.status
        assert "data" == resp.data
        assert "GET" == open_url.call_args[1]["method"]
        assert "example.com/path" == open_url.call_args[1]["url"]

    def test_non_20x_status(self, mocker):
        open_url = mocker.patch.object(http, "open_url")
        open_url.side_effect = HTTPError(
            "url", 404, "missing", {}, None,
        )

        resp = http.request("GET", "example.com/bad")

        assert 404 == resp.status
        assert "missing" == resp.data
        assert "GET" == open_url.call_args[1]["method"]
        assert "example.com/bad" == open_url.call_args[1]["url"]

    def test_url_error(self, mocker):
        open_url = mocker.patch.object(http, "open_url")
        open_url.side_effect = URLError("Invalid")

        with pytest.raises(errors.HttpError):
            http.request("GET", "example.com/bad")

    def test_payload_no_headers(self, mocker):
        data_resp = mocker.Mock()
        data_resp.read.return_value = "data"
        data_resp.getcode.return_value = 200
        open_url = mocker.patch.object(http, "open_url")
        open_url.return_value = data_resp

        http.request("PUT", "example.com/path", payload=dict(a=2))

        assert "PUT" == open_url.call_args[1]["method"]
        assert "example.com/path" == open_url.call_args[1]["url"]
        assert '{"a":2}' == open_url.call_args[1]["data"]
        headers = open_url.call_args[1]["headers"]
        assert {"content-type": "application/json"} == headers

    def test_payload_with_headers(self, mocker):
        data_resp = mocker.Mock()
        data_resp.read.return_value = "data"
        data_resp.getcode.return_value = 200
        open_url = mocker.patch.object(http, "open_url")
        open_url.return_value = data_resp

        http.request(
            "PUT", "example.com/path", payload=dict(b=4), headers=dict(h="v"),
        )

        assert "PUT" == open_url.call_args[1]["method"]
        assert "example.com/path" == open_url.call_args[1]["url"]
        assert '{"b":4}' == open_url.call_args[1]["data"]
        headers = open_url.call_args[1]["headers"]
        assert {"content-type": "application/json", "h": "v"} == headers

    def test_payload_overrides_data(self, mocker):
        data_resp = mocker.Mock()
        data_resp.read.return_value = "data"
        data_resp.getcode.return_value = 200
        open_url = mocker.patch.object(http, "open_url")
        open_url.return_value = data_resp

        http.request(
            "PUT", "example.com/path", payload=dict(a=2), data="data",
        )

        assert "PUT" == open_url.call_args[1]["method"]
        assert "example.com/path" == open_url.call_args[1]["url"]
        assert '{"a":2}' == open_url.call_args[1]["data"]
        headers = open_url.call_args[1]["headers"]
        assert {"content-type": "application/json"} == headers

    def test_data(self, mocker):
        data_resp = mocker.Mock()
        data_resp.read.return_value = "data"
        data_resp.getcode.return_value = 200
        open_url = mocker.patch.object(http, "open_url")
        open_url.return_value = data_resp

        http.request("PUT", "example.com/path", data="data")

        assert "PUT" == open_url.call_args[1]["method"]
        assert "example.com/path" == open_url.call_args[1]["url"]
        assert "data" == open_url.call_args[1]["data"]
        assert open_url.call_args[1]["headers"] is None

    def test_kwargs(self, mocker):
        data_resp = mocker.Mock()
        data_resp.read.return_value = "data"
        data_resp.getcode.return_value = 200
        open_url = mocker.patch.object(http, "open_url")
        open_url.return_value = data_resp

        http.request("PUT", "example.com/path", a=3, b="f")

        assert "PUT" == open_url.call_args[1]["method"]
        assert "example.com/path" == open_url.call_args[1]["url"]
        assert 3 == open_url.call_args[1]["a"]
        assert "f" == open_url.call_args[1]["b"]

    def test_cert_error_ssl_module_present(self, mocker):
        open_url = mocker.patch.object(http, "open_url")
        open_url.side_effect = ssl.CertificateError("Invalid")

        with pytest.raises(errors.HttpError):
            http.request("GET", "example.com/bad")

    def test_cert_error_ssl_module_absent(self, mocker):
        class Dummy(Exception):
            pass

        open_url = mocker.patch.object(http, "open_url")
        open_url.side_effect = ssl.CertificateError("Invalid")
        mocker.patch.object(http, "CertificateError", Dummy)

        with pytest.raises(ssl.CertificateError):
            http.request("GET", "example.com/bad")
