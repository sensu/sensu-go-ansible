# -*- coding: utf-8 -*-
# Copyright: (c) 2019, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from datetime import datetime

import os
import sys

# Import utils package which resides above us because it's reusable.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../../.."))
import _utils as utils  # noqa


testinfra_hosts = ['backend']


def agents_from_api(host):
    addr = utils.ip_addr(host)
    events = utils.api(addr, "api/core/v2/namespaces/default/events")
    events = [e for e in events if e["timestamp"] > datetime.utcnow().timestamp() - 10]
    events = [e for e in events if e["check"]["metadata"]["name"] == "keepalive"]
    registered_agents = [e["entity"] for e in events]

    return registered_agents


class TestBackend:
    def test_all_agents_sent_keepalive(self, host):
        registered_agents = agents_from_api(host)
        registered_agent_names = [a["system"]["hostname"] for a in registered_agents]
        actual_agents = host.ansible.get_variables()["groups"]["agents"]
        assert sorted(actual_agents) == sorted(registered_agent_names)

    def test_agent_settings(self, host):
        registered_agents = agents_from_api(host)
        actual_agents = host.ansible.get_variables()["groups"]["agents"]
        for host in actual_agents:
            agent = next(a for a in registered_agents if a["system"]["hostname"] == host)
            assert agent["user"] == "agent"
            assert agent["deregister"] is False
