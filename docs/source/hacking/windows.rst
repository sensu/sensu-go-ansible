Windows things
==============

Working with Windows is a bit different from what most of us are probably used
to since there is no package manager to delegate installation to and services
behave a bit differently. Here is a collection of things that might come in
handy when working with installation and agent role.


Adding new Sensu Go version manually
------------------------------------

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


Automating version sync
-----------------------

Because manually extracting the product code from the msi archive is not
something we would like to devote our lives to, we created a script that knows
how to do two things:

 1. It can check if the variable file is missing any upstream versions.
 2. It can automatically update the Windows variable file.

To check for the missing versions in out current file, we can run the following
command::

   $ tools/windows-versions.py check roles/install/vars/Windows.yml
   The following versions are missing: 6.2.3.3986, 6.2.4.4013, 6.2.5.4040
   The following versions are obsolete: 5.20.0.12118, 5.20.1.12427

This command will check if our variable file contains any outdated versions and
if it is missing any new versions Sensu released since our last update. The
command also exits with a non-zero status if action is required, which is great
for CI/CD usage.

We also added the common invocation to the Makefile, which makes running check
as simple as::

   $ make check_windows_versions

Once we know our variables and upstream availability diverged, we can run the
update command to get things back in sync::

   $ tools/windows-versions.py update roles/install/vars/Windows.yml

This command will download any missing packages, extract product codes from
them, and update the variable file. By default, temporary files are put ino the
``/tmp`` directory, but this is configurable via the ``--cache`` command-line
switch.

As with the check command, we also added the common invocation to the Makefile,
which allows us to update the variable file with a simple make run::

   $ make update_windows_versions

.. note::

   The update process needs ``msiinfo`` executable. The package should be
   available for most mainstream Linux distributions.

Once the update is over, we must commit the changes to the variable file and we
are done.
