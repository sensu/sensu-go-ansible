# -*- coding: utf-8 -*-
# Copyright: (c) 2019, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    client, errors,
)


class TestToken:
    def test_get_valid_token(self, mocker):
        open_url = mocker.patch.object(client, "open_url")
        open_url.return_value.read.return_value = '{"access_token": "token"}'

        c = client.Client("http://example.com/", "user", "pass")

        assert "token" == c.token
        assert 1 == open_url.call_count
        print(open_url.call_args)
        assert ("http://example.com/auth",) == open_url.call_args[0]
        assert "user" == open_url.call_args[1]["url_username"]
        assert "pass" == open_url.call_args[1]["url_password"]

    def test_cache_token(self, mocker):
        open_url = mocker.patch.object(client, "open_url")
        open_url.return_value.read.return_value = '{"access_token": "token"}'

        c = client.Client("http://example.com/", "user", "pass")
        for i in range(5):
            c.token

        assert 1 == open_url.call_count

    def test_login_failure(self, mocker):
        open_url = mocker.patch.object(client, "open_url")
        open_url.side_effect = URLError("Invalid")

        with pytest.raises(errors.ClientError):
            client.Client("http://example.com/", "user", "pass").token


class TestRequest:
    def test_valid_json(self, mocker):
        auth_resp = mocker.Mock()
        auth_resp.read.return_value = '{"access_token": "token"}'
        data_resp = mocker.Mock()
        data_resp.read.return_value = '{"some": "json"}'
        data_resp.getcode.return_value = 200
        open_url = mocker.patch.object(client, "open_url")
        open_url.side_effect = auth_resp, data_resp

        resp = client.Client("http://ex.com/", "user", "pass").request(
            "GET", "/path",
        )

        assert 200 == resp.status
        assert '{"some": "json"}' == resp.data
        assert {"some": "json"} == resp.json

        url = open_url.call_args[1]["url"]
        assert "http://ex.com/api/core/v2/path" == url

        auth = open_url.call_args[1]["headers"]["Authorization"]
        assert "Bearer token" == auth

    def test_invalid_json(self, mocker):
        auth_resp = mocker.Mock()
        auth_resp.read.return_value = '{"access_token": "token"}'
        data_resp = mocker.Mock()
        data_resp.read.return_value = "Bad json {}"
        data_resp.getcode.return_value = 200
        open_url = mocker.patch.object(client, "open_url")
        open_url.side_effect = auth_resp, data_resp

        resp = client.Client("http://ex.com/", "user", "pass").get("/path")

        assert 200 == resp.status
        assert "Bad json {}" == resp.data
        assert resp.json is None

    def test_non_200(self, mocker):
        auth_resp = mocker.Mock()
        auth_resp.read.return_value = '{"access_token": "token"}'
        data_resp = HTTPError("url", 404, '{"msg": "missing item"}', {}, None)
        open_url = mocker.patch.object(client, "open_url")
        open_url.side_effect = auth_resp, data_resp

        resp = client.Client("http://ex.com/", "user", "pass").get("/path")

        assert 404 == resp.status
        assert '{"msg": "missing item"}' == resp.data
        assert {"msg": "missing item"} == resp.json

    def test_set_json_content_type(self, mocker):
        auth_resp = mocker.Mock()
        auth_resp.read.return_value = '{"access_token": "token"}'
        data_resp = mocker.Mock()
        data_resp.read.return_value = '{"some": "json"}'
        data_resp.getcode.return_value = 201
        open_url = mocker.patch.object(client, "open_url")
        open_url.side_effect = auth_resp, data_resp

        resp = client.Client("http://ex.com/", "user", "pass").put("/path", {})

        data = open_url.call_args[1]["data"]
        print(data)
        assert "{}" == data

        content_type = open_url.call_args[1]["headers"]["content-type"]
        assert "application/json" == content_type

    def test_url_error(self, mocker):
        auth_resp = mocker.Mock()
        auth_resp.read.return_value = '{"access_token": "token"}'
        open_url = mocker.patch.object(client, "open_url")
        open_url.side_effect = auth_resp, URLError("Invalid")

        with pytest.raises(errors.ClientError):
            client.Client("http://ex.com/", "user", "pass").get("/path")

    def test_namespace_url_construction(self, mocker):
        auth_resp = mocker.Mock()
        auth_resp.read.return_value = '{"access_token": "token"}'
        data_resp = mocker.Mock()
        data_resp.read.return_value = ""
        data_resp.getcode.return_value = 204
        open_url = mocker.patch.object(client, "open_url")
        open_url.side_effect = auth_resp, data_resp

        resp = client.Client(
            "http://ex.com/", "user", "pass", "ns",
        ).delete("/path")

        url = open_url.call_args[1]["url"]
        assert "http://ex.com/api/core/v2/namespaces/ns/path" == url
        assert 204 == resp.status
