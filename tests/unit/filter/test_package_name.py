# Copyright: (c) 2020, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible_collections.sensu.sensu_go.plugins.filter import package_name


class TestPackageName:
    def test_yum_latest_version(self):
        assert "package" == package_name.package_name(
            "yum", "package", "latest", "latest",
        )

    def test_yum_latest_build(self):
        assert "package-123" == package_name.package_name(
            "yum", "package", "123", "latest",
        )

    def test_yum_selected_build(self):
        assert "package-123-456" == package_name.package_name(
            "yum", "package", "123", "456",
        )

    def test_yum_ignore_build_if_latest_version(self):
        assert "package" == package_name.package_name(
            "yum", "package", "latest", "456",
        )

    def test_apt_latest_version(self):
        assert "package" == package_name.package_name(
            "apt", "package", "latest", "latest",
        )

    def test_apt_latest_build(self):
        assert "package=123-*" == package_name.package_name(
            "apt", "package", "123", "latest",
        )

    def test_apt_selected_build(self):
        assert "package=123-456" == package_name.package_name(
            "apt", "package", "123", "456",
        )

    def test_apt_ignore_build_if_latest_version(self):
        assert "package" == package_name.package_name(
            "apt", "package", "latest", "456",
        )
