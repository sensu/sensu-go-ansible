# -*- coding: utf-8 -*-
# Copyright: (c) 2019, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    client, errors, http
)


class TestToken:
    def test_get_valid_token(self, mocker):
        request = mocker.patch.object(http, "request")
        request.return_value = http.Response(200, '{"access_token": "token"}')

        c = client.Client("http://example.com/", "user", "pass")

        assert "token" == c.token
        assert 1 == request.call_count
        assert ("GET", "http://example.com/auth") == request.call_args[0]
        assert "user" == request.call_args[1]["url_username"]
        assert "pass" == request.call_args[1]["url_password"]

    def test_cache_token(self, mocker):
        request = mocker.patch.object(http, "request")
        request.return_value = http.Response(200, '{"access_token": "token"}')

        c = client.Client("http://example.com/", "user", "pass")
        for i in range(5):
            c.token

        assert 1 == request.call_count

    def test_login_failure_bad_status(self, mocker):
        request = mocker.patch.object(http, "request")
        request.return_value = http.Response(500, '{"access_token": "token"}')

        with pytest.raises(errors.SensuError, match="500"):
            client.Client("http://example.com/", "user", "pass").token

    def test_login_failure_bad_json(self, mocker):
        request = mocker.patch.object(http, "request")
        request.return_value = http.Response(200, "{ not a json }")

        with pytest.raises(errors.SensuError, match="JSON"):
            client.Client("http://example.com/", "user", "pass").token

    def test_login_failure_missing_token(self, mocker):
        request = mocker.patch.object(http, "request")
        request.return_value = http.Response(200, '{"access_bla": "token"}')

        with pytest.raises(errors.SensuError, match="token"):
            client.Client("http://example.com/", "user", "pass").token


class TestRequest:
    def test_request_payload(self, mocker):
        request = mocker.patch.object(http, "request")
        request.side_effect = (
            http.Response(200, '{"access_token": "token"}'),
            http.Response(200, "data"),
        )

        client.Client("http://example.com/", "user", "pass").request(
            "PUT", "/path", dict(some="payload"),
        )

        request.assert_called_with(
            "PUT", "http://example.com/path",
            payload=dict(some="payload"),
            headers=dict(Authorization="Bearer token"),
        )

    def test_request_no_payload(self, mocker):
        request = mocker.patch.object(http, "request")
        request.side_effect = (
            http.Response(200, '{"access_token": "token"}'),
            http.Response(200, "data"),
        )

        client.Client("http://example.com/", "user", "pass").request(
            "PUT", "/path",
        )

        request.assert_called_with(
            "PUT", "http://example.com/path", payload=None,
            headers=dict(Authorization="Bearer token"),
        )


class TestGet:
    def test_get(self, mocker):
        c = client.Client("http://example.com/", "user", "pass")
        c.request = mocker.Mock()

        c.get("/path")

        c.request.assert_called_with("GET", "/path")


class TestPut:
    def test_put(self, mocker):
        c = client.Client("http://example.com/", "user", "pass")
        c.request = mocker.Mock()

        c.put("/path", {})

        c.request.assert_called_with("PUT", "/path", {})


class TestDelete:
    def test_delete(self, mocker):
        c = client.Client("http://example.com/", "user", "pass")
        c.request = mocker.Mock()

        c.delete("/path")

        c.request.assert_called_with("DELETE", "/path")
