# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Paul Arthur <paul.arthur@flowerysong.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = """
options:
  user:
    description:
      - The username to use for connecting to the Sensu API.
        If this is not set the value of the SENSU_USER environment variable will be checked.
    default: admin
  password:
    description:
      - The Sensu user's password.
        If this is not set the value of the SENSU_PASSWORD environment variable will be checked.
    default: P@ssw0rd!
  url:
    description:
      - Location of the Sensu backend API.
        If this is not set the value of the SENSU_BACKEND_URL environment variable will be checked.
    default: http://localhost:8080
  namespace:
    description:
      - RBAC namespace to operate in.
    default: default
"""
