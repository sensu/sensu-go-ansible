Release policy
==============

Our release policy could be summarized as:

 1. We only support latest stable release.
 2. We create new bugfix and feature releases as things progress and not on a
    fixed schedule.
 3. We support deprecated content for at least a year and a half since its
    deprecation.
 4. We have no plans on releasing version 2.0.0 anytime soon and are fully
    commited on making current version of collection work on all supported
    Sensu Go versions.


Supported releases
------------------

As already stated, we only support latest stable version of Sensu Go Ansible
Collection. Currently, this means that only latest 1.x.y version is supported.

Once we next major version of collection, we will continue to backport
security fixes to previous major version 1 for at least half a year. No new
features will be backported.


Release schedule
----------------

To get new features and bugfixes to our users as soon as possible, we have no
fixed release schedule. Instead, we create a new release after each
significant change (bugfix or added feature). We may delay release for a day
or two if we have a few thing lined up to reduce the administrative load.


Compatibility
-------------

Sensu Go Ansible Collection follows `semantic versioning`_. In short, we
guarantee backward compatibility between releases with the same major version
number. In practice, this means that if we have a playbook that works with
some version of Sensu Go Ansible Collection, it will continue to work with
newer versions up until major version changes.

.. _semantic versioning: https://semver.org/

We do not guarantee forward compatibility (we are adding new modules in
releases that increment minor version number). Downgrading between patch
versions should be safe, but we would advice against it because patch releases
can potentially contain important security fixes.
