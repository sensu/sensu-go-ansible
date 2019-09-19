# -*- coding: utf-8 -*-
# Copyright: (c) 2019, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import requests


def latest_sensu_available():
    """Access webpage to learn what the latest Sensu version is"""
    res = requests.get("https://docs.sensu.io/sensu-go/latest", allow_redirects=False)
    latest_url = res.headers.get("Location", "unknown").strip("/")
    return latest_url.split("/")[-1]


testinfra_hosts = ["latest_components"]
LATEST_VERSION = latest_sensu_available()


def test_backend_installed(host):
    assert host.exists("sensu-backend")
    assert "sensu-backend version {0}".format(LATEST_VERSION) in \
           host.check_output("sensu-backend version")


def test_agent_installed(host):
    assert host.exists("sensu-agent")
    assert "sensu-agent version {0}".format(LATEST_VERSION) in \
           host.check_output("sensu-agent version")


def test_cli_installed(host):
    assert host.exists("sensuctl")
    assert "sensuctl version {0}".format(LATEST_VERSION) in \
           host.check_output("sensuctl version")
