Installation
============

We can install Sensu Go Ansible collection using the ``ansible-galaxy`` tool
that comes bundled with Ansible. This tool can install Ansible collections
from different sources.


Installing from Ansible Galaxy
------------------------------

`Ansible Galaxy`_ is the default source of Ansible collections for the
``ansible-galaxy`` tool. We can install Sensu Go Ansible collection by
running::

   $ ansible-galaxy collection install sensu.sensu_go

.. _Ansible Galaxy: https://galaxy.ansible.com

After the command finishes, we will have the latest version of the Sensu Go
Ansible collection installed and ready to be used.

We can also install a specific version of the collection by appending a
version after the name::

   $ ansible-galaxy collection install sensu.sensu_go:1.0.0

.. note::

   ``ansible-galaxy`` command will not overwrite the existing collection if it
   is already installed. We can change this default behavior by adding a
   ``--force`` command line switch::

      $ ansible-galaxy collection install --force sensu.sensu_go:1.0.0

The official Ansible documentation contains more information about the
installation options in the `Using collections`_ document.

.. _Using collections:
   https://docs.ansible.com/ansible/latest/user_guide/collections_using.html#installing-collections


Installing from Automation Hub
------------------------------

If we have a valid Red Hat subscription, we can also install Sensu Go Ansible
collection from Red Hat Ansible Automation Hub. But before we can do that, we
need to tell Ansible about the second source of collections. We do this by
placing the following content into the
:download:`ansible.cfg <../examples/installation/ansible.cfg>` configuration
file:

.. literalinclude:: ../examples/installation/ansible.cfg
   :language: ini


Make sure you replace the ``token`` value in the above configuration with the
value obtained from the `token Automation Hub UI`_.

.. _token Automation Hub UI:
   https://cloud.redhat.com/ansible/automation-hub/token

From here on, we can follow the steps from the previous section.


Installing from a local file
----------------------------

This last method of installation might come in handy in situations where our
Ansible control node cannot access Ansible Galaxy or Automation Hub.

First, we need to download the Sensu Go Ansible collection archive from the
GitHub `releases page`_ and then transfer that archive to the Ansible control
node. Once we have that archive on our control node, we can install the Sensu
Go collection by running::

   $ ansible-galaxy collection install path/to/sensu-sensu_go-1.0.0.tar.gz

.. _releases page:
   https://github.com/sensu/sensu-go-ansible/releases
