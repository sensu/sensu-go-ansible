# -*- coding: utf-8 -*-
# Copyright: (c) 2019, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import json

from ansible.module_utils.urls import open_url
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.six.moves.urllib.parse import quote

from ansible_collections.sensu.sensu_go.plugins.module_utils import (
    errors, response, debug
)


def _abort(msg, *args, **kwargs):
    raise errors.ClientError(msg.format(*args, **kwargs))


class Client:
    def __init__(self, address, username, password, namespace=None):
        self.address = address.rstrip("/")
        self.username = username
        self.password = password

        if namespace:
            self.url_template = "{0}/api/core/v2/namespaces/{1}{{0}}".format(
                self.address, quote(namespace, safe=""),
            )
        else:
            self.url_template = "{0}/api/core/v2{{0}}".format(self.address)

        self._token = None  # Login when/if required

    @property
    def token(self):
        if not self._token:
            self._token = self._login()
        return self._token

    def _login(self):
        try:
            resp = open_url(
                "{0}/auth".format(self.address), force_basic_auth=True,
                url_username=self.username, url_password=self.password,
            )
            token = json.loads(resp.read())["access_token"]
            debug.log("Login token: [{0}/auth] {1}***", self.address, token[:5])
            return token
        except URLError as e:
            debug.log("Login failed: [{0}/auth] {1}", self.address, e.reason)
            _abort("Login failed: {}", e.reason)

    def request(self, method, path, payload=None):
        arguments = dict(
            url=self.url_template.format(path),
            method=method,
            headers={"Authorization": "Bearer {0}".format(self.token)},
            data=None,
        )
        if payload is not None:
            arguments["headers"]["content-type"] = "application/json"
            arguments["data"] = json.dumps(payload)

        try:
            resp = open_url(**arguments)
            resp = response.Response(resp.getcode(), resp.read())
            debug.log_request(arguments, resp)
            return resp
        except HTTPError as e:
            # This is not an error, since client consumers might be able to
            # work around/expect non 20x codes.
            resp = response.Response(e.code, e.reason)
            debug.log_request(arguments, resp)
            return resp
        except URLError as e:
            debug.log_request(arguments, comment=e.reason)
            _abort("{} request failed: {}", method, e.reason)

    def get(self, path):
        return self.request("GET", path)

    def put(self, path, payload):
        return self.request("PUT", path, payload)

    def delete(self, path):
        return self.request("DELETE", path)
