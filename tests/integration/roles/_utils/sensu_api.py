# -*- coding: utf-8 -*-
# Copyright: (c) 2019, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import base64
import json

from .docker import container_exec


def api_auth(addr):
    """Authenticate against Sensu API, leverage proxy container"""
    output = container_exec(
        "proxy",
        "curl -s -H 'Authorization: {0}' http://{1}:8080/auth > /dev/null".format(
            "Basic {0}".format(base64.b64encode(b"admin:P@ssw0rd!").decode('utf-8')), addr)
    )
    token = json.loads(output)["access_token"]
    return "Bearer {0}".format(token)


def api(addr, path):
    """Obtain access token then invoke Sensu REST API endpoint"""
    output = container_exec(
        "proxy",
        "curl -s -H 'Authorization: {0}' http://{1}:8080/{2} > /dev/null".format(api_auth(addr), addr, path)
    )
    return json.loads(output)
