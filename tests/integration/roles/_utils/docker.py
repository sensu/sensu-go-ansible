# -*- coding: utf-8 -*-
# Copyright: (c) 2019, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import docker


def container(name):
    """Container handle"""
    return docker.from_env().containers.get(name)


def container_exec(container_name, command):
    """Execute command on a container"""
    _code, output = container(container_name).exec_run(command)
    return output.decode("UTF-8").strip()
