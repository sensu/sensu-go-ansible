Sensu Go agent role
===================

This role installs, configures and starts the ``sensu-agent`` service.


Example playbook
----------------

The most basic
:download:`agent playbook <../../examples/roles/agent.yaml>` looks like this:

.. literalinclude:: ../../examples/roles/agent.yaml
   :language: yaml

This playbook will install the latest stable version of the Sensu Go agent
and configure it. We can customize the agent's configuration by adding more
options to the *agent_config* variable.


Agent configuration options
---------------------------

The *agent_config* variable can contain any option that is valid for the Sensu
Go agent version we are installing. All valid options are listed in the
`official Sensu documentation`_.

.. _official Sensu documentation:
   https://docs.sensu.io/sensu-go/latest/reference/agent/#configuration

.. note::

   Role copies the key-value pairs from the *agent_config* variable verbatim
   to the configuration file. This means that we must copy the key names
   **exactly** as they appear in the configuration reference. In a way, the
   *agent_config* variable should contain a properly indented copy of the
   ``/etc/sensu/agent.yml`` file.


Tested Platforms (CI/CD)
------------------------

+-------+--------------+-----------------------------------+
| OS    | distribution | versions                          |
+=======+==============+===================================+
| Linux | CentOS       | 7                                 |
|       +--------------+-----------------------------------+
|       | RedHat       | 7, 8                              |
|       +--------------+-----------------------------------+
|       | Debian       | 9, 10                             |
|       +--------------+-----------------------------------+
|       | Ubuntu       | 14.04, 16.04, 18.04               |
+-------+--------------+-----------------------------------+
