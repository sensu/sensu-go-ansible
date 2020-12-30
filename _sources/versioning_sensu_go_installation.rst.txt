Versioning Sensu Go installation
================================

When dealing with software installation, we want to pin the versions of our
components as tightly as possible. In the first part of this guide, we will
look at how we can pin the Sensu Go version when using Ansible. We will focus
our attention on updates in the second part of this guide.


Initial install
---------------

The :doc:`backend </roles/backend>` and :doc:`agent </roles/agent>` roles both
use the :doc:`install </roles/install>` role for installing required
components. And the installation Ansible role consults three variables when
determining what component version to install: **version**, **build**, and
**channel**.

In the vast majority of scenarios, we can set the **version** variable and
leave the build and channel variables set to their default values:

.. code-block:: yaml

   - name: Install, configure and run Sensu agents
     hosts: agents
     become: true
     tasks:
       - name: Install agent
         include_role:
           name: sensu.sensu_go.agent
         vars:
           version: 6.1.4

When we run the previous playbook, Ansible will install the latest 6.1.4
version build from the `stable channel`_. And since stable channel only
contains one package build per released version, we pinned down the Sensu Go
version to a single package.

Unstable versions of Sensu Go can have more than one build associated with
them. In scenarios where we are dealing with prerelease versions, we can use
the **build** variable to make installation predictable or use an older
package build:


.. code-block:: yaml

   - name: Install, configure and run Sensu agents
     hosts: agents
     become: true
     tasks:
       - name: Install agent
         include_role:
           name: sensu.sensu_go.agent
         vars:
           channel: testing
           version: 6.2.0
           build: 3881

.. note::

   The installation role ignores both the **channel** and the **build**
   variables values when installing the Sensu Go agent on Windows. For the
   time being, Windows users can only install stable versions with the Sensu
   Go agent role.

We can also install the latest available version if we omit the version
variable or set it to ``latest``. But we strongly advise against this approach
since we may inadvertently update our Sensu Go version when all we wanted to
do is update our configuration file.


Updating existing installation
------------------------------

If you think updating our Sensu Go installation is as simple as bumping the
version number and rerunning the playbook, you are almost right. Ansible will
update and restart the updated Sensu Go backend or agent services, but it will
not run any version-specific migration tasks.

Thankfully, for most updates, restarting services is all that is needed. For
the rest of the cases, update instructions are usually straightforward. You
can find them all in the `Sensu Go documentation`_.


Downgrading versions
--------------------

The Sensu Go Ansible Collection does not support downgrades. You might be able
to install an older version of Sensu Go, but there are no guarantees that your
installation will still work.


.. _stable channel:
   https://packagecloud.io/sensu/stable

.. _Sensu Go documentation:
   https://docs.sensu.io/sensu-go/latest/operations/maintain-sensu/upgrade/
