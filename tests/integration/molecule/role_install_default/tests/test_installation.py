# -*- coding: utf-8 -*-
# Copyright: (c) 2019, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


def test_backend_installed(host):
    assert host.exists("sensu-backend")


def test_agent_installed(host):
    assert host.exists("sensu-agent")


def test_cli_installed(host):
    assert host.exists("sensuctl")
