Sensu Go backend role
=====================

This role installs, configures and starts the ``sensu-backend`` service.


Example playbook
----------------

The most basic
:download:`backend playbook <../../examples/roles/backend.yaml>` looks like
this:

.. literalinclude:: ../../examples/roles/backend.yaml
   :language: yaml

This playbook will install the latest stable version of the Sensu Go backend
and configure it. We can customize the backend's configuration by adding more
options to the *backend_config* variable.


Backend configuration options
-----------------------------

The *backend_config* variable can contain any option that is valid for the
Sensu Go backend version we are installing. All valid options are listed in
the `official Sensu documentation`_. 

.. _official Sensu documentation:
   https://docs.sensu.io/sensu-go/latest/reference/backend/#configuration

.. note::

   Role copies the key-value pairs from the *backend_config* variable verbatim
   to the configuration file. This means that we must copy the key names
   **exactly** as they appear in the configuration reference. In a way, the
   *backend_config* variable should contain a properly indented copy of the
   ``/etc/sensu/backend.yml`` file.

Users of Sensu Go >= 5.16 have two additional variables at their disposal that
control the first-time backend initialization:

.. list-table::
   :header-rows: 1
   :widths: 25 30 45

   * - Variable
     - Default
     - Description

   * - cluster_admin_username
     - admin
     - Initial admin user to create when initializing backend for the first
       time.

   * - cluster_admin_password
     - P@ssw0rd!
     - Initial admin password to create when initializing backend for the
       first time.

On Sensu Go version below 5.16, these two variables have no effect since
default admin credentials are baked into the Sensu Go backend.


Securing Sensu Go backend
-------------------------

This role enables users to establish secure end-to-end communications of the
components that comprise the Sensu Go backend. The user needs to supply the
paths to the PKI files by placing the appropriate public and private key files
somewhere within the Ansible playbook search path. They then need to reference
these paths in the appropriate inventory variables, as described below.

.. note::

   All of the files referenced in each of the following subsections need to be
   supplied. If even a single file is missing or not defined, the play will
   fail. If none of the variables within a subsection is defined, those
   services will be configured without the secure communication.

Etcd peer communication
^^^^^^^^^^^^^^^^^^^^^^^

To secure the etcd communication, create the appropriate files for the PKI
and define **all** of the following variables:

.. list-table::
   :header-rows: 1
   :widths: 25 30 45

   * - Variable
     - Examples
     - Description

   * - etcd_cert_file
     - files/pki/etcd-client.crt
     - Path to the certificate used for SSL/TLS connections **to** etcd. This
       is a client certificate.

   * - etcd_key_file
     - files/pki/etcd-client.key
     - Path to the private key for the etcd client certificate file. Must be
       unencrypted.

   * - etcd_trusted_ca_file
     - files/pki/client-ca.crt
     - Path to the trusted certificate authority for the etcd client
       certificates.

   * - etcd_peer_cert_file
     - files/pki/etcd-peer.crt
     - Path to the certificate used for SSL/TLS connections between peers.
       This will be used both for listening on the peer address as well as
       sending requests to other peers.

   * - etcd_peer_key_file
     - files/pki/etcd-peer.key
     - Path to the peer certificate's key. Must be unencrypted.

   * - etcd_peer_trusted_ca_file
     - files/pki/etcd-peer-ca.crt
     - Path to the trusted certificate authority for the peer certificates.

Backend API
^^^^^^^^^^^

To secure the Sensu Go backend API communication, create the appropriate files
for the PKI and define **all** of the following variables:

.. list-table::
   :header-rows: 1
   :widths: 25 30 45

   * - Variable
     - Examples
     - Description

   * - api_cert_file
     - files/pki/sensu-api.crt
     - Path to the certificate used to secure the Sensu Go API.

   * - api_key_file
     - files/pki/sensu-api.key
     - Path to the private key corresponding to the Sensu Go API certificate.
       Must be unencrypted.

   * - api_trusted_ca_file
     - files/pki/sensu-api-ca.crt
     - Path to the trusted certificate authority for the Sensu Go API
       certificates.

Dashboard
^^^^^^^^^

To secure the Sensu dashboard communication, create the appropriate files for the
PKI and define **all** of the following variables:

.. list-table::
   :header-rows: 1
   :widths: 25 30 45

   * - Variable
     - Examples
     - Description

   * - dashboard_cert_file
     - files/pki/sensu-dashboard.crt
     - Path to the certificate used for SSL/TLS connections to the dashboard.

   * - dashboard_key_file
     - files/pki/sensu-dashboard.key
     - Path to the private key corresponding to the dashboard certificate.
       Must be unencrypted.

The role will automatically configure the dashboard endpoint to use HTTPS,
e.g.: `https://localhost:3000`.


Tested Platforms (CI/CD)
------------------------

+-------+--------------+-----------------------------------+
| OS    | distribution | versions                          |
+=======+==============+===================================+
| Linux | CentOS       | 7, 8                              |
|       +--------------+-----------------------------------+
|       | RedHat       | 7, 8                              |
|       +--------------+-----------------------------------+
|       | Debian       | 9, 10                             |
|       +--------------+-----------------------------------+
|       | Ubuntu       | 14.04, 16.04, 18.04               |
+-------+--------------+-----------------------------------+
