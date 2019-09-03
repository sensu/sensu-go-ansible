# -*- coding: utf-8 -*-
# Copyright: (c) 2019, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import json


class Response:
    def __init__(self, status, data):
        self.status = status
        self.data = data
        try:
            self.json = json.loads(data)
        except ValueError:  # Cannot use JSONDecodeError here (python 2)
            self.json = None
