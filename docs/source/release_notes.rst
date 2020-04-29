Release notes
=============

Version 1.4.0 -- Keeping up with the world
------------------------------------------

Main changes in this release are related to updates in the Sensu Go's web API
that broke our change detection.

**New features:**

* Add support for RHEL and CentOS 8.

**Bug fixes:**

* Fix resource metadata comparison on Sensu Go 5.19.0 and newer.
* Update entity comparator to handle new fields.


Version 1.3.1 -- Bug fixing galore
----------------------------------

This release makes it possible to use the *asset* module when replacing the
deprecated, single-build assets that were created by means other than Ansible.

**Bug fixes:**

* Do not die when encountering a deprecated asset format.
* Update return value documentation for info modules.
* Add Sensu Go 5.17.x and 5.18.x to the test suite and remove the unsupported
  versions (5.14.2 and lower).
* Update the role metadata with proper platform markers.
* Remove unsupported Ubuntu versions from the test suite.


Version 1.3.0 -- Authenticating with style on Debian
----------------------------------------------------

Sensu Go 5.15.0 gained an API key authentication method and the Ansible
collection finally caught up. This means that we can now replace *user* and
*password* authentication parameters with a single *api_key* value.

And the other big news is the addition of Debian support to the `install`
role.

**New features:**

* Add API key authentication support.
* Add support for Debian installation.


Version 1.2.0 -- Building support for builds
--------------------------------------------

This release adds support for specifying builds when installing various Sensu
Go components.

**New features:**

* Add *build* variable to the *install* role that further pins down the
  package version that gets installed.


Version 1.1.1 -- Python 2 is Still a Thing
------------------------------------------

This is a bugfix release that makes sure the Sensu collection is working when
Ansible control node uses Python 2.

**New features:**

* Add support for RHEL 7 to the install role (thanks, @danragnar).

**Bug fixes:**

* Accept *str* and *unicode* instance as a valid string in *bonsai_asset*
  action plugin.


Version 1.1 -- Hello Sensu Go 5.16
----------------------------------

This is the first release that supports installing Sensu Go 5.16.

**New features:**

* Support for Sensu Go 5.16 initialization in backend role.
* Support for external datastore management using *datastore* and
  *datastore_info* modules.

**Bug fixes:**

* Reintroduce namespace support to *bonsai_asset* module (thanks, @jakeo)


Version 1.0 -- Rising From The Ashes
------------------------------------

This is the initial stable release of the Sensu Go Ansible Collection. It
contains roles for installing and configuring Sensu Go backends and agents and
a set of modules for managing Sensu Go resources.

Where does the release name comes from? We took an existing Ansible Collection
that `@flowerysong`_ wrote, gave it a thorough tune-up and added a
comprehensive test suite. And now, it is ready to face the world!

.. _@flowerysong: https://github.com/flowerysong/ansible-sensu-go

