Windows things
==============

Working with Windows is a bit different from what most of us are probably used
to since there is no package manager to delegate installation to and services
behave a bit differently. Here is a collection of things that might come in
handy when working with installation and agent role.


Adding new Sensu Go version
---------------------------

As already state, Windows has no built-in package manager backed by a
repository, which means we have to do a bit more work when installing
packages. And this is why our installation role contains a few pieces of
information about the available Sensu Go agent packages.

We can add a new version of Sensu Go for Windows using the following steps:

 1. Find the version and build we are interested in on packagecloud_.
 2. Download the x64 and x86 msi files from the download page. Use the
    download URL from the `installation guide`_ as a base and adjust as
    needed.
 3. Extract product codes from the msi packages (document author used orca msi
    editor, would be very much interested in a PowerShell script).
 4. Add a new entry to the roles/install/vars/Windows.yml file.

.. _packagecloud: https://packagecloud.io/sensu/stable
.. _installation guide: https://docs.sensu.io/sensu-go/latest/operations/deploy-sensu/install-sensu/#install-sensu-agents
