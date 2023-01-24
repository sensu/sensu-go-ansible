=======================================
Scale_Computing.Hypercore Release Notes
=======================================

.. contents:: Topics


v1.13.2
=======

Release Summary
---------------

Support for latest Ansible and Rocky and Alma linux


Minor Changes
-------------

- Added support for Rocky and Alma linux
- Added support for ansible 2.14

v1.13.1
=======

Release Summary
---------------

Support for latest Ansible


Minor Changes
-------------

- Added support for ansible 2.13
- Removed support for CentOS 8

v1.13.0
=======

Release Summary
---------------

Bonsai asset definitions can be downloaded on controller or remote nodes 

A user can decide if Bonsai asset definitions should be downloaded to
remote nodes or the controller node. This is useful, but not limited to,
in case that the controller node's Internet connection is unstable or in
general worse than that of the remote nodes.


Minor Changes
-------------

- Added argument remote_on inside bonsai_asset module

v1.12.1
=======

Release Summary
---------------

Keeping up with updates


Minor Changes
-------------

- Add Sensu Go 6.5.5 Windows metadata
- Add sensu Go 6.6.2 Windows metadata

v1.12.0
=======

Release Summary
---------------

Keeping up with the updates

In this release, community contributed support for the OracleLinux. We
added a few tests to catch if things break in the future and this is
about it. And while we were at work, we also added support for Sensu Go
6.4.0 and 6.4.1 on Windows.


Minor Changes
-------------

- Add Sensu Go 6.4.0 Windows metadata.
- Add Sensu Go 6.4.1 Windows metadata.
- Add support for OracleLinux.

v1.11.1
=======

Release Summary
---------------

Sensu Go 6.3.0 is here

For this release, we only updated the list of available Sensu Go agent
versions for Windows, and made sure collection works with the latest
Sensu Go version.


Minor Changes
-------------

- Update list of available Sensu Go agent packages for Windows installations (added 6.3.0).

v1.11.0
=======

Release Summary
---------------

Validate all the things!

If you ever thought to yourself, "Ansible does not yell enough at me,"
we have some great news. The Sensu Go Ansible Collection gained role
argument specifications, making it possible to validate variable values
before executing a role. You are welcome ;)


Minor Changes
-------------

- Add argument specification to the agent role.
- Add argument specification to the backend role.
- Add argument specification to the install role.

v1.10.0
=======

Release Summary
---------------

Authentication, authentication on the wall, Who has Access to Them All?

New modules allow Sensu Go users to configure authentication within
their Ansible playbooks. The users can authenticate via external
authentication providers such as Lightweight Directory Access Protocol (LDAP),
Active Directory (AD), or OpenID Connect 1.0 protocol (OIDC).


Minor Changes
-------------

- Add modules for managing Sensu Go authentication providers.

New Modules
-----------

- sensu.sensu_go.ad_auth_provider - Manage Sensu AD authentication provider
- sensu.sensu_go.auth_provider_info - List Sensu authentication providers
- sensu.sensu_go.ldap_auth_provider - Manage Sensu LDAP authentication provider
- sensu.sensu_go.oidc_auth_provider - Manage Sensu OIDC authentication provider

v1.9.4
======

Release Summary
---------------

Opening Windows for real

This is a bugfix release that makes sure Sensu Go Ansible Collection
can operate even in the absence of the Windows Ansible Collection
(assuming we do not want to manage agents on Windows hosts, that is).


Bugfixes
--------

- Make sure we lazy-load Windows-related content.

v1.9.3
======

Release Summary
---------------

Opening Windows

The only change in this release is removal of the ``ansible.windows``
dependency. This should allow users that only use certified collections
to install and use the collection.


v1.9.2
======

Release Summary
---------------

A fresh batch of updates

For this release, we only updated the list of available Sensu Go agent
versions for Windows.


v1.9.1
======

Release Summary
---------------

Containerize all the things

There are two main reasons for this release. We made sure the Sensu Go
Ansible Collection works with development version of Ansible (upcoming
ansible-core 2.11). And we added enough metadata to the collection that
ansible-builder can create an execution environment with the Sensu Go
Ansible Collection without having to manually specify dependencies.


Bugfixes
--------

- Add ansible.windows dependency that we forgot to add when we introducted the Sensu Go agent installation on Windows.

v1.9.0
======

Release Summary
---------------

Multi-cluster visibility with federation

Two new module pairs allow Sensu Go users to configure federation from
the comfort of their Ansible playbooks.


Minor Changes
-------------

- Add modules for managing Sensu Go clusters.
- Add modules for managing etcd replicatiors, which form the basis of the Sensu Go federation.
- Update list of available Sensu Go agent packages for Windows installations.

Bugfixes
--------

- Allow downgrading Sensu Go packages on Linux distributions that use yum or dnf for package management.

New Modules
-----------

- sensu.sensu_go.cluster - Manage Sensu Go clusters
- sensu.sensu_go.cluster_info - List available Sensu Go clusters
- sensu.sensu_go.etcd_replicator - Manage Sensu Go etcd replicators
- sensu.sensu_go.etcd_replicator_info - List Sensu Go etcd replicators

v1.8.0
======

Release Summary
---------------

Supporting hashed user passwords

Starting with this release, Sensu Go users can use password hashes
directly when manipulating role-based access control resources.


Minor Changes
-------------

- Add support for hashed password in user module.

Bugfixes
--------

- Make it possible to use modules on Sensu Go backends with no version number.
- Mimic actual responses when user module runs in check mode.

v1.7.2
======

Release Summary
---------------

Be kind

The main thing in this release is a small adjustment of our code of
conduct that is a bit more generic and less event-focused.


Minor Changes
-------------

- List version 6.2.1 and 6.2.2 in Windows lookup table.
- Specify minimal python version for modules.
- Update code of conduct.

v1.7.1
======

Release Summary
---------------

Slow and steady

There are no major new features in this release, just honest little
fixes that should make using Sensu Go Ansible Collection a bit more
pleasant.


Minor Changes
-------------

- Add module return value samples.
- List version 6.2.0 and 6.1.3 in Windows lookup table.

v1.7.0
======

Release Summary
---------------

Say hello to Amazon Linux and Windows

As the title suggests, we worked hard to bring you two new supported
platforms to the Sensu Go Ansible Colletions. And yes, all your
existing playbooks still work.All you need to do is run them against
the right host and voila ;)


Minor Changes
-------------

- Add support for installing Sensu Go agents on Windows.
- Add support for installing Sensu Go on Amazon Linux.

v1.6.1
======

Release Summary
---------------

Comparing entities is hard

This is a bugfix release that makes sure agent entity changes are
properly detected.


Bugfixes
--------

- Make subscriptions comparison insensitive to ordering.
- Make sure agent entities handle *entity:{name}* automatic subscriptions.

v1.6.0
======

Release Summary
---------------

Our little secret

This release contains a few new modules that allow you to manage all
things related to the Sensu Go secrets: from adding secrets providers
to passing secrets to resources that know how to use them.


Minor Changes
-------------

- Add modules for managing Sensu Go secret providers.
- Add modules for managing Sensu Go secrets.
- Add support for secrets to check module.
- Add support for secrets to mutator module.
- Add support for secrets to pipe handler module.

New Modules
-----------

- sensu.sensu_go.secret - Manage Sensu Go secrets
- sensu.sensu_go.secret_info - List available Sensu Go secrets
- sensu.sensu_go.secrets_provider_env - Manage Sensu Env secrets provider
- sensu.sensu_go.secrets_provider_info - List Sensu secrets providers
- sensu.sensu_go.secrets_provider_vault - Manage Sensu VaultProvider secrets provider

v1.5.0
======

Release Summary
---------------

Self-signed security

The primary focus of this release is to enable configuration of Sensu
Go backends that use certificates that are not considered trusted when
using system-provided CA bundle.


Minor Changes
-------------

- Allow modules to supply custom CA bundle for backend certificate validation or skip the validation entirely.

Bugfixes
--------

- Expand documentation about the *check_hooks* parameter in the check module.
- Explain how the resource name parameter is used and what invariants need to hold in order for the Sensu Go to consider it a valid name.

v1.4.2
======

Release Summary
---------------

Break the fall

There is really only one reason for this release: making sure user
management works with Sensu Go 5.21.0 and newer. And while the
upstream did break the API, we did not, so all your playbooks should
function as nothing happened. We had to add a *bcrypt* dependency to
our collection so make sure it is installed on hosts that will execute
the user module.


Bugfixes
--------

- Make sure check module is as idempotent as possible.
- Make user module compatible with Sensu Go >= 5.21.0.

v1.4.1
======

Release Summary
---------------

Maintenance is the name of the game

There are no nothing earth-shattering changes in this release, just
honest little bug fixes and compatibility improvements.

**NOTE:** The *sensu.sensu_go.user* module currently **DOES NOT** work
on Sensu Go 5.21.0 and later. This is a know issue that will be fixed
as soon as the updated user-related backend API endpoints are
documented.


Bugfixes
--------

- Ensure backend initialization properly reports changed state.
- Make API key authentication work even for regular users with limited permissions.
- Make sure event module always returns a predicted result.
- Make user module fully-idempotent. Previous versions did not properly detect the password changes.
- Update the datastore module to cope with the minor API changes.
- Use fully-qualified collection names in module documentation.

v1.4.0
======

Release Summary
---------------

Keeping up with the world

Main changes in this release are related to updates in the Sensu Go's
web API that broke our change detection.


Minor Changes
-------------

- Add support for RHEL and CentOS 8.

Bugfixes
--------

- Fix resource metadata comparison on Sensu Go 5.19.0 and newer.
- Update entity comparator to handle new fields.

v1.3.1
======

Release Summary
---------------

Bug fixing galore

This release makes it possible to use the *asset* module when
replacing the deprecated, single-build assets that were created by
means other than Ansible.


Bugfixes
--------

- Add Sensu Go 5.17.x and 5.18.x to the test suite and remove the unsupported versions (5.14.2 and lower).
- Do not die when encountering a deprecated asset format.
- Remove unsupported Ubuntu versions from the test suite.
- Update return value documentation for info modules.
- Update the role metadata with proper platform markers.

v1.3.0
======

Release Summary
---------------

Authenticating with style on Debian

Sensu Go 5.15.0 gained an API key authentication method and the
Ansible collection finally caught up. This means that we can now
replace *user* and *password* authentication parameters with a single
*api_key* value.

And the other big news is the addition of Debian support to the
`install` role.


Minor Changes
-------------

- Add API key authentication support.
- Add support for Debian installation.

v1.2.0
======

Release Summary
---------------

Building support for builds

This release adds support for specifying builds when installing
various Sensu Go components.


Minor Changes
-------------

- Add *build* variable to the *install* role that further pins down the package version that gets installed.

v1.1.1
======

Release Summary
---------------

Python 2 is Still a Thing

This is a bugfix release that makes sure the Sensu collection is
working when Ansible control node uses Python 2.


Minor Changes
-------------

- Add support for RHEL 7 to the install role (thanks, @danragnar).

Bugfixes
--------

- Accept *str* and *unicode* instance as a valid string in *bonsai_asset* action plugin.

v1.1.0
======

Release Summary
---------------

Hello Sensu Go 5.16

This is the first release that supports installing Sensu Go 5.16.


Minor Changes
-------------

- Support for Sensu Go 5.16 initialization in backend role.
- Support for external datastore management using *datastore* and *datastore_info* modules.

Bugfixes
--------

- Reintroduce namespace support to *bonsai_asset* module (thanks, @jakeo)

New Modules
-----------

- sensu.sensu_go.datastore - Manage Sensu external datastore providers
- sensu.sensu_go.datastore_info - List external Sensu datastore providers

v1.0.0
======

Release Summary
---------------

Rising From The Ashes

This is the initial stable release of the Sensu Go Ansible Collection.
It contains roles for installing and configuring Sensu Go backends and
agents and a set of modules for managing Sensu Go resources.

Where does the release name comes from? We took an existing Ansible
Collection that @flowerysong wrote, gave it a thorough tune-up and
added a comprehensive test suite. And now, it is ready to face the
world!

