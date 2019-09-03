# -*- coding: utf-8 -*-
# Copyright: (c) 2019, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible_collections.sensu.sensu_go.plugins.module_utils import response


class TestInit:
    def test_with_valid_json(self):
        resp = response.Response(201, '{"some": ["json", "data", 3]}')

        assert 201 == resp.status
        assert '{"some": ["json", "data", 3]}' == resp.data
        assert {"some": ["json", "data", 3]} == resp.json

    def test_with_invalid_json(self):
        resp = response.Response(404, "")

        assert 404 == resp.status
        assert "" == resp.data
        assert resp.json is None
