Installing Sensu Go Backend
===========================

There are three steps that we need to go through when we are setting up the
Sensu Go backend. We need to:

1. prepare the inventory file,
2. write the playbook, and
3. run the created playbook.

Let us have a look at each of the steps in greater detail.


Creating the inventory file
---------------------------

We will create an inventory file with a single group of hosts called
*backends*. The *backends* group will, in turn, contain a single host named
*my_backend* (it should be painfully apparent by now that a developer wrote
this documentation ;). An inventory file that fits the description above would
look something like
:download:`this <../../examples/scenarios/installing_backend/inventory.yaml>`:

.. literalinclude:: ../../examples/scenarios/installing_backend/inventory.yaml
   :language: yaml

The key-value pairs under the *my_backend* key describe the host-specific
variable assignments. In the example above, we are telling Ansible that it can
reach *my_backend* host by establishing an ssh-connection to the
``vagrant@192.168.50.4``.

.. note::

   We are using a  YAML inventory format in this document. Feel free to use
   any other Ansible-supported form if this one does not feel right to you.


With the inventory file being taken care of, we can now focus on creating a
playbook for the installation process.


Writing the installation playbook
---------------------------------

Thanks to the *sensu.sensu_go.backend* Ansible role, writing a playbook for
the Sensu Go backend installation is a relatively straightforward task. It all
comes down to a few lines like this:

.. code-block:: yaml

   ---
   - name: Install, configure and run Sensu backend
     hosts: backends
     become: true

     tasks:
       - name: Install backend
         include_role:
           name: sensu.sensu_go.backend

If we run the playbook above, Ansible will install the latest stable version
of Sensu Go backend on all of the hosts in the *backends* inventory group with
the default configuration. And while this is fine for the sandbox
environments, we will want to, at least partially, pin the package version and
adjust the backend configuration.

We have two variables available for limiting the package version: *version*
and *build*. We can set only *version* or *version* and *build*, but setting
*build* on itself is pointless and is ignored by the Sensu Go collection
roles. For example, pinning Sensu Go to version ``5.16.1`` would look somewhat
like this:

.. code-block:: yaml

   ---
   - name: Install, configure and run Sensu backend
     hosts: backends
     become: true

     tasks:
       - name: Install backend
         include_role:
           name: sensu.sensu_go.backend
         vars:
           version: 5.16.1

And just for the sake of completeness, this is how we would go about pinning
version down to the specific build:

.. code-block:: yaml

   ---
   - name: Install, configure and run Sensu backend
     hosts: backends
     become: true

     tasks:
       - name: Install backend
         include_role:
           name: sensu.sensu_go.backend
         vars:
           version: 5.16.1
           build: 8521

There is also a third variable available, called *channel*. We can use this
variable to tell the Sensu Go roles which repository to use when installing
the packages. Most users will want to leave this variable set to its default
value of ``stable``.

.. note::

   The stable package channel usually contains only one version build. What
   this means is that pinning only the version number should suffice in the
   vast majority of cases.

The last thing we need to do is get rid of the default configuration. And we
can do that by modifying the *backend_config* variable. All we need to do is
to stuff this variable with key-value pairs of configuration options. The end
result should look like
:download:`this <../../examples/scenarios/installing_backend/playbook.yaml>`:

.. literalinclude:: ../../examples/scenarios/installing_backend/playbook.yaml
   :language: yaml

.. note::

   What constitutes a valid backend configuration file is Sensu Go
   version-dependent, so make sure to check the official documentation for the
   version you use when setting the *backend_config* variable.

If we are installing a version of Sensu Go that is greater or equal to 5.16.0,
we can also set the initial username and password for the backend. The two
variables that control this are *cluster_admin_username* and
*cluster_admin_password*. Their default values are ``admin`` and ``P@ssw0rd!``
in order to be compatible with the older Sensu Go releases.

Now that we adequately pinned the version number and specified the
configuration, we can finally run the playbook.


Running the playbook
--------------------

At this point, we are ready to let Ansible deploy the Sensu Go backend while
we take a quick snack. All that separates us from the cookie we started
thinking about when we were two sentences into this document is this command::

   $ ansible-playbook -i inventory.yaml playbook.yaml

And this is it. Congratulations on making all the way through! You can find
the complete example along with some extras (like Vagrant configuration) in
the `example folder`_.

.. _example folder: https://link.to/github/example
