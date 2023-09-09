Installing a TLS Secured Sensu Go Backend Cluster
===========================

In production environments, you typically want to take advantage of the Sensu Go's use of etcd for high availability fail-over, and TLS encryption of all communication endpoints. All of this can be achieved using a slightly more complicated playbook, making use of the backend_config directive to express the Sensu backend configuration options.  In fact you can use the Ansible playbook to generate self-signed certs using your own private CA too to automatea cluster staging environment.

The procedure follows the same lines as the the stand-alone backend scenario, but the playbook used here will have several more steps, so its best to read through that scenario first.

Creating the inventory file
---------------------------

We will create an inventory file with both a *backends* and *agents* groups defined. The *backends* group will, in turn, contain the cluster hosts with the prefix
*sensu-cluster*. An inventory file that fits the description above would
look something like
:download:`this <../../examples/scenarios/installing_backend_cluster/inventory.yaml>`:

.. literalinclude:: ../../examples/scenarios/installing_backend_cluster/inventory.yaml
   :language: yaml

The key-value pairs under the *sensu-clusterXX* key describe the host-specific
variable assignments. In the example above, we are telling Ansible that it can
reach *sensu-cluster0* host by establishing an ssh-connection to the
``vagrant@192.168.50.20``.

.. note::

   We are using a  YAML inventory format in this document. Feel free to use
   any other Ansible-supported form if this one does not feel right to you.


With the inventory file being taken care of, we can now focus on creating a
playbook for the installation process.


A secure cluster playbook
---------------------------------
Generating self-signed TLS certificates can be somewhat tedious to do by hand but can be automated easily as part of an Ansible playbook.  The example cluster playbook below is made up of several tasks to ensure self-signed certificates are put in place prior to starting up the Sensu backend and Sensu agents.



:download:`this <../../examples/scenarios/installing_backend_cluster/playbook.yaml>`:

.. literalinclude:: ../../examples/scenarios/installing_backend_cluster/playbook.yaml
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


Running the playbook
--------------------

At this point, we are ready to let Ansible deploy the Sensu Go backend while
we take a quick snack. All that separates us from the cookie we started
thinking about when we were two sentences into this document is this command::

   $ ansible-playbook -i inventory.yaml playbook.yaml

The `sensu-ca.pem` certificate authority needed to verify the certificates will be located in the .keys sub-directory. You can now use this CA file and make TLS secured connections to any of the backend clusters using the ip addresses used in the inventory file.

And this is it. Congratulations on making all the way through! You can find
the complete example along with some extras (like Vagrant configuration) in
the `example folder`_.

.. _example folder: https://link.to/github/example
