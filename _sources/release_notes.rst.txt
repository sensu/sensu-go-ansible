Release notes
=============

Version 1.8.0 -- Supporting hashed user passwords
-------------------------------------------------

Starting with this release, Sensu Go users can use password hashes directly
when manipulating role-based access control resources.

**New features:**

* Add support for hashed password in user module.

**Bug fixes:**

* Mimic actual responses when user module runs in check mode.
* Make it possible to use modules on Sensu Go backends with no version number.


Version 1.7.2 -- Be kind
------------------------

The main thing in this release is a small adjustment of our code of conduct
that is a bit more generic and less event-focused.

**Bug fixes:**

* List version 6.2.1 and 6.2.2 in Windows lookup table.
* Specify minimal python version for modules.
* Update code of conduct.


Version 1.7.1 -- Slow and steady
--------------------------------

There are no major new features in this release, just honest little fixes that
should make using Sensu Go Ansible Collection a bit more pleasant.

**Bug fixes:**

* List version 6.2.0 and 6.1.3 in Windows lookup table.
* Add module return value samples.


Version 1.7.0 -- Say hello to Amazon Linux and Windows
------------------------------------------------------

As the title suggests, we worked hard to bring you two new supported platforms
to the Sensu Go Ansible Colletions. And yes, all your existing playbooks still
work.All you need to do is run them against the right host and voila ;)

**New features:**

* Add support for installing Sensu Go on Amazon Linux.
* Add support for installing Sensu Go agents on Windows.



Version 1.6.1 -- Comparing entities is hard
-------------------------------------------

This is a bugfix release that makes sure agent entity changes are properly
detected.

**Bug fixes:**

* Make subscriptions comparison insensitive to ordering.
* Make sure agent entities handle *entity:{name}* automatic subscriptions.


Version 1.6.0 -- Our little secret
----------------------------------

This release contains a few new modules that allow you to manage all things
related to the Sensu Go secrets: from adding secrets providers to passing
secrets to resources that know how to use them.

**New features:**

* Add modules for managing Sensu Go secret providers.
* Add modules for managing Sensu Go secrets.
* Add support for secrets to pipe handler module.
* Add support for secrets to check module.
* Add support for secrets to mutator module.


Version 1.5.0 -- Self-signed security
-------------------------------------

The primary focus of this release is to enable configuration of Sensu Go
backends that use certificates that are not considered trusted when using
system-provided CA bundle.

**New features:**

* Allow modules to supply custom CA bundle for backend certificate validation
  or skip the validation entirely.

**Bug fixes:**

* Expand documentation about the *check_hooks* parameter in the check module.
* Explain how the resource name parameter is used and what invariants need to
  hold in order for the Sensu Go to consider it a valid name.

Version 1.4.2 -- Break the fall
-------------------------------

There is really only one reason for this release: making sure user management
works with Sensu Go 5.21.0 and newer. And while the upstream did break the
API, we did not, so all your playbooks should function as nothing happened. We
had to add a *bcrypt* dependency to our collection so make sure it is
installed on hosts that will execute the user module.

**Bug fixes:**

* Make sure check module is as idempotent as possible.
* Make user module compatible with Sensu Go >= 5.21.0.


Version 1.4.1 -- Maintenance is the name of the game
----------------------------------------------------

There are no nothing earth-shattering changes in this release, just honest
little bug fixes and compatibility improvements.

**NOTE:** The *sensu.sensu_go.user* module currently **DOES NOT** work on
Sensu Go 5.21.0 and later. This is a know issue that will be fixed as soon as
the updated user-related backend API endpoints are documented.


**Bug fixes:**

* Make sure event module always returns a predicted result.
* Make user module fully-idempotent. Previous versions did not properly detect
  the password changes.
* Use fully-qualified collection names in module documentation.
* Ensure backend initialization properly reports changed state.
* Make API key authentication work even for regular users with limited
  permissions.
* Update the datastore module to cope with the minor API changes.


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

