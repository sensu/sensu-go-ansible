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


class TestAuthHeader:
    def test_using_valid_token(self, mocker):
        request = mocker.patch.object(http, "request")
        request.return_value = http.Response(200, '{"access_token": "token"}')

        c = client.Client(
            "http://example.com/", "user", "pass", None, True, None,
        )

        assert dict(Authorization="Bearer token") == c.auth_header
        assert 1 == request.call_count
        assert ("GET", "http://example.com/auth") == request.call_args[0]
        assert "user" == request.call_args[1]["url_username"]
        assert "pass" == request.call_args[1]["url_password"]

    def test_cache_auth_headers_with_token(self, mocker):
        request = mocker.patch.object(http, "request")
        request.return_value = http.Response(200, '{"access_token": "token"}')

        c = client.Client(
            "http://example.com/", "user", "pass", None, True, None,
        )
        for i in range(5):
            c.auth_header

        assert 1 == request.call_count

    def test_login_failure_token_bad_status(self, mocker):
        request = mocker.patch.object(http, "request")
        request.return_value = http.Response(500, '{"access_token": "token"}')

        with pytest.raises(errors.SensuError, match="500"):
            client.Client(
                "http://example.com/", "user", "pass", None, True, None,
            ).auth_header

    def test_login_failure_token_bad_json(self, mocker):
        request = mocker.patch.object(http, "request")
        request.return_value = http.Response(200, "{ not a json }")

        with pytest.raises(errors.SensuError, match="JSON"):
            client.Client(
                "http://example.com/", "user", "pass", None, True, None,
            ).auth_header

    def test_login_failure_token_missing_token(self, mocker):
        request = mocker.patch.object(http, "request")
        request.return_value = http.Response(200, '{"access_bla": "token"}')

        with pytest.raises(errors.SensuError, match="token"):
            client.Client(
                "http://example.com/", "user", "pass", None, True, None,
            ).auth_header


class TestVersion:
    def test_valid_version(self, mocker):
        c = client.Client("http://example.com/", "u", "p", None, True, None)
        mocker.patch.object(c, "get").return_value = http.Response(
            200, '{"sensu_backend":"5.21.0#sha-here"}',
        )

        assert c.version == "5.21.0"

    def test_valid_version_is_cached(self, mocker):
        c = client.Client("http://example.com/", "u", "p", None, True, None)
        get = mocker.patch.object(c, "get")
        get.return_value = http.Response(
            200, '{"sensu_backend":"5.21.0#sha-here"}',
        )

        for i in range(4):
            c.version

        get.assert_called_once()

    def test_non_200_response(self, mocker):
        c = client.Client("http://example.com/", "u", "p", None, True, None)
        mocker.patch.object(c, "get").return_value = http.Response(
            400, '{"sensu_backend":"5.21.0#sha-here"}',
        )

        with pytest.raises(errors.SensuError, match="400"):
            c.version

    def test_bad_json_response(self, mocker):
        c = client.Client("http://example.com/", "u", "p", None, True, None)
        mocker.patch.object(c, "get").return_value = http.Response(
            200, '"sensu_backend',
        )

        with pytest.raises(errors.SensuError, match="JSON"):
            c.version

    def test_missing_backend_version_in_response(self, mocker):
        c = client.Client("http://example.com/", "u", "p", None, True, None)
        mocker.patch.object(c, "get").return_value = http.Response(200, '{}')

        with pytest.raises(errors.SensuError, match="backend"):
            c.version

    def test_invalid_version(self, mocker):
        c = client.Client("http://example.com/", "u", "p", None, True, None)
        mocker.patch.object(c, "get").return_value = http.Response(
            200, '{"sensu_backend":"devel"}',
        )

        assert c.version == c.BAD_VERSION


class TestRequest:
    def test_request_payload_token(self, mocker):
        request = mocker.patch.object(http, "request")
        request.side_effect = (
            http.Response(200, '{"access_token": "token"}'),
            http.Response(200, "data"),
        )

        client.Client(
            "http://example.com/", "user", "pass", None, True, None,
        ).request("PUT", "/path", dict(some="payload"))

        request.assert_called_with(
            "PUT", "http://example.com/path",
            payload=dict(some="payload"),
            headers=dict(Authorization="Bearer token"),
            validate_certs=True,
            ca_path=None,
        )

    def test_request_payload_api_key(self, mocker):
        request = mocker.patch.object(http, "request")
        request.return_value = http.Response(200, "data")

        client.Client(
            "http://example.com/", None, None, "key", False, None,
        ).request("PUT", "/path", dict(some="payload"))

        request.assert_called_once_with(
            "PUT", "http://example.com/path",
            payload=dict(some="payload"),
            headers=dict(Authorization="Key key"),
            validate_certs=False,
            ca_path=None,
        )

    def test_request_no_payload_token(self, mocker):
        request = mocker.patch.object(http, "request")
        request.side_effect = (
            http.Response(200, '{"access_token": "token"}'),
            http.Response(200, "data"),
        )

        client.Client(
            "http://example.com/", "user", "pass", None, True, "/ca",
        ).request("PUT", "/path")

        request.assert_called_with(
            "PUT", "http://example.com/path", payload=None,
            headers=dict(Authorization="Bearer token"),
            validate_certs=True,
            ca_path="/ca",
        )

    def test_request_no_payload_api_key(self, mocker):
        request = mocker.patch.object(http, "request")
        request.return_value = http.Response(200, "data")

        client.Client(
            "http://example.com/", "u", "p", "key", False, "/ca",
        ).request("PUT", "/path")

        request.assert_called_once_with(
            "PUT", "http://example.com/path", payload=None,
            headers=dict(Authorization="Key key"),
            validate_certs=False,
            ca_path="/ca",
        )

    @pytest.mark.parametrize("status", [401, 403])
    def test_request_bad_credentials(self, status, mocker):
        request = mocker.patch.object(http, "request")
        request.return_value = http.Response(status, "data")

        with pytest.raises(errors.SensuError, match="credentials"):
            client.Client(
                "http://example.com/", None, None, "key", True, None,
            ).request("PUT", "/path", dict(some="payload"))

        request.assert_called_once_with(
            "PUT", "http://example.com/path",
            payload=dict(some="payload"),
            headers=dict(Authorization="Key key"),
            validate_certs=True,
            ca_path=None,
        )


class TestGet:
    def test_get(self, mocker):
        c = client.Client(
            "http://example.com/", "user", "pass", None, True, None,
        )
        c.request = mocker.Mock()

        c.get("/path")

        c.request.assert_called_with("GET", "/path")


class TestPut:
    def test_put(self, mocker):
        c = client.Client(
            "http://example.com/", "user", "pass", None, True, None,
        )
        c.request = mocker.Mock()

        c.put("/path", {})

        c.request.assert_called_with("PUT", "/path", {})


class TestDelete:
    def test_delete(self, mocker):
        c = client.Client(
            "http://example.com/", "user", "pass", None, True, None,
        )
        c.request = mocker.Mock()

        c.delete("/path")

        c.request.assert_called_with("DELETE", "/path")


class TestValidateAuthData:
    def test_valid_creds(self, mocker):
        request = mocker.patch.object(http, "request")
        request.return_value = http.Response(200, None)
        c = client.Client(
            "http://example.com/", "user", "pass", None, True, None,
        )

        result = c.validate_auth_data("check_user", "check_pass")

        assert result
        assert 1 == request.call_count
        assert ("GET", "http://example.com/auth/test") == request.call_args[0]
        assert "check_user" == request.call_args[1]["url_username"]
        assert "check_pass" == request.call_args[1]["url_password"]

    def test_invalid_creds(self, mocker):
        request = mocker.patch.object(http, "request")
        request.return_value = http.Response(401, None)
        c = client.Client(
            "http://example.com/", "user", "pass", None, True, None,
        )

        result = c.validate_auth_data("check_user", "check_pass")

        assert not result
        assert 1 == request.call_count
        assert ("GET", "http://example.com/auth/test") == request.call_args[0]
        assert "check_user" == request.call_args[1]["url_username"]
        assert "check_pass" == request.call_args[1]["url_password"]

    def test_broken_backend(self, mocker):
        request = mocker.patch.object(http, "request")
        request.return_value = http.Response(500, None)
        c = client.Client(
            "http://example.com/", "user", "pass", None, True, None,
        )

        with pytest.raises(errors.SensuError, match="500"):
            c.validate_auth_data("check_user", "check_pass")
