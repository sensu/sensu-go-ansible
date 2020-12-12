Sensu Go install role
=====================

This role installs selected Sensu Go components from the official precompiled
packages.

.. note::

   This role only configures your package manager (like yum or apt) and
   installs the binaries. It does **not** configure anything and it does
   **not** run any services.


Example playbook
----------------

The next :download:`playbook <../../examples/roles/install.yaml>` demonstrates
how to install different versions of Sensu components from specific channels.

.. literalinclude:: ../../examples/roles/install.yaml
   :language: yaml


Role Variables
--------------

This role consults the following variables to determine what packages to
install:

.. list-table::
   :header-rows: 1
   :widths: 25 30 45

   * - Variable
     - Default value
     - Description

   * - components
     - - sensu-go-backend
       - sensu-go-agent
       - sensu-go-cli
     - List of components to install. Valid values are ``sensu-go-backend``,
       ``sensu-go-agent`` and ``sensu-go-cli``.

   * - channel
     - stable
     - Repository channel that serves as a source of packages. We can see all the
       available channels on packagecloud_ site.

   * - version
     - latest
     - Package version to install. Can be any valid version string such as
       ``5.14.2`` or special value ``latest``.

   * - build
     - latest
     - Package build to install. Can be any valid build string such as
       ``8290`` or a special value ``latest``. If the *version* variable is
       set to ``latest``, this variable is ignored and the latest available
       build is installed.

   * - packagecloud_auth
     - ""
     - Credentials to use when setting up Sensu Go repos. For publicly
       available repos, this can be left empty. For private repos, this should
       be set to the value of the read token, folloved by the ``:@``. Example:
       ``ofb9123457acdddef6734524:@``.

.. _packagecloud: https://packagecloud.io/sensu


Tested Platforms (CI/CD)
------------------------

+-------+--------------+-----------------------------------+
| OS    | distribution | versions                          |
+=======+==============+===================================+
| Linux | Amazon       | 1, 2                              |
|       +--------------+-----------------------------------+
|       | CentOS       | 7, 8                              |
|       +--------------+-----------------------------------+
|       | RedHat       | 7, 8                              |
|       +--------------+-----------------------------------+
|       | Debian       | 9, 10                             |
|       +--------------+-----------------------------------+
|       | Ubuntu       | 14.04, 16.04, 18.04               |
+-------+--------------+-----------------------------------+
