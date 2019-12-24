Release notes
=============

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

