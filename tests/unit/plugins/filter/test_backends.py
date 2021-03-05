from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys

import pytest

from ansible_collections.sensu.sensu_go.plugins.filter import backends

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestBackends:
    def test_backends_in_groups_no_ssl(self):
        hostvars = {
            "1.2.3.4": {"inventory_hostname": "1.2.3.4"},
            "1.2.3.5": {"inventory_hostname": "1.2.3.5"},
            "1.2.3.6": {"inventory_hostname": "1.2.3.6"},
            "1.2.3.7": {"inventory_hostname": "1.2.3.7"},
        }
        groups = {"backends": ["1.2.3.4", "1.2.3.5"]}

        assert backends.backends(hostvars, groups) == [
            "ws://1.2.3.4:8081",
            "ws://1.2.3.5:8081",
        ]

    def test_backends_in_groups_ssl(self):
        hostvars = {
            "1.2.3.4": {"inventory_hostname": "1.2.3.4"},
            "1.2.3.5": {"inventory_hostname": "1.2.3.5"},
            "1.2.3.6": {
                "inventory_hostname": "1.2.3.6",
                "api_key_file": "path/to/key.file",
            },
            "1.2.3.7": {"inventory_hostname": "1.2.3.7"},
        }
        groups = {"backends": ["1.2.3.6"]}

        assert backends.backends(hostvars, groups) == ["wss://1.2.3.6:8081"]

    def test_backends_not_in_groups(self):
        hostvars = {
            "1.2.3.4": {"inventory_hostname": "1.2.3.4"},
            "1.2.3.5": {"inventory_hostname": "1.2.3.5"},
            "1.2.3.6": {"inventory_hostname": "1.2.3.6"},
            "1.2.3.7": {"inventory_hostname": "1.2.3.7"},
        }
        groups = {}

        assert backends.backends(hostvars, groups) == []
