Updating playbooks for Sensu Go 6
=================================

One of the more significant changes in Sensu Go 6 is how we manage agents and
agent entities. In previous Sensu Go versions, configuration for both agents and
agent entities resided in the agent's configuration file. A typical Ansible
playbook for managing Sensu Go 5 agents looked like this:

.. code-block:: yaml

   - name: Install, configure and run Sensu agents
     hosts: agents
     become: true
     tasks:
       - name: Install agent
         include_role:
           name: sensu.sensu_go.agent
         vars:
           version: 5.21.2
           agent_config:
             name: my-agent
             backend-url:
               - ws://backend.host:8081
             keepalive-interval: 5
             keepalive-timeout: 10
             deregister: true
             subscriptions:
               - linux

In Sensu Go 6, we manage the entity representing the agent via the API, just
like all other Sensu Go resources. Unfortunately, this means that we must move
specific configuration options from the ``agent_config`` variable into a
separate task in our play for managing monitoring configuration:

.. code-block:: yaml

   - name: Install, configure and run Sensu agents
     hosts: agents
     become: true
     tasks:
       - name: Install agent
         include_role:
           name: sensu.sensu_go.agent
         vars:
           version: 6.0.0
           agent_config:
             name: my-agent
             backend-url:
               - ws://backend.host:8081
             keepalive-interval: 5
             keepalive-timeout: 10

   - name: Configure monitoring resources
     hosts: localhost
     tasks:
       - name: Add subscriptions to agent entity
         sensu.sensu_go.entity:
           name: my-agent
           entity_class: agent
           deregister: true
           subscriptions:
             - linux

Options that we should move are **annotations**, **deregister**,
**deregistration-handler**, **labels**, **redact**, and **subscriptions**. We
can copy over most of the options from one play into another verbatim. The only
exception is the **deregistration-handler** agent configuration option that
corresponds to the **deregistration_handler** entity module parameter.

.. note::

   If we leave entity-related configuration options in the agent's configuration
   file, Sensu Go will use them when creating an entity. Sensu Go will ignore
   any subsequent updates of the configuration file.
