# -*- coding: utf-8 -*-
# Copyright: (c) 2019, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

testinfra_hosts = ["agents"]


def test_config_file(host):
    conf = host.file("/etc/sensu/agent.yml")
    assert conf.contains("^backend-url:\n( )+- ws://upstream-backend:4321")
    assert not conf.contains("^log-level:")


def test_log_file(host):
    log = host.file("/var/log/sensu/sensu-agent.log")
    assert log.exists
    assert log.contains("successfully connected")
    assert log.contains("sending keepalive")
