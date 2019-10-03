# -*- coding: utf-8 -*-
# Copyright: (c) 2019, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import json
import os
import sys

# Import utils package which resides above us because it's reusable.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../../.."))
import _utils as utils  # noqa


testinfra_hosts = ["backends"]


def test_backend_healthy(host):
    addr = utils.ip_addr(host)
    output = utils.container_exec("proxy", "curl -s http://{0}:8080/health > /dev/null".format(addr))
    health = json.loads(output)
    for cluster in health["ClusterHealth"]:
        assert cluster["Healthy"] is True
        assert cluster["Err"] == ""


def test_api_with_authentication(host):
    addr = utils.ip_addr(host)
    handlers = utils.api(addr, "api/core/v2/namespaces/default/handlers")
    assert handlers == []


def test_config_file(host):
    conf = host.file("/etc/sensu/backend.yml")
    assert not conf.contains("^debug:")
    assert not conf.contains("^log-level:")
