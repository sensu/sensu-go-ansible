# -*- coding: utf-8 -*-
# Copyright: (c) 2019, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

OLDER_VERSION = "5.12.0"


def test_backend_installed(host):
    assert host.exists("sensu-backend")
    assert "sensu-backend version {0}".format(OLDER_VERSION) in \
           host.check_output("sensu-backend version")


def test_agent_installed(host):
    assert host.exists("sensu-agent")
    assert "sensu-agent version {0}".format(OLDER_VERSION) in \
           host.check_output("sensu-agent version")


def test_cli_installed(host):
    assert host.exists("sensuctl")
    assert "sensuctl version {0}".format(OLDER_VERSION) in \
           host.check_output("sensuctl version")
