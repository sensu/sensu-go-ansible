Monitoring hosts
================

Once we have our Sensu Go backend ready, we can start installing agents on the
hosts that we would like to monitor. We will once again do this in three
stages. We will:

1. populate the inventory,
2. create the playbook, and
3. execute the playbook.

Let us start with the Ansible inventory construction.


Building the inventory file
---------------------------

We will expand the inventory file from the Installing Sensu Go Backend
document. Reasons for this will become apparent once we get to the playbook
section. We will add a new group called *agents* and populate it with two
hosts that we would like to monitor. Once we get everything right, the
inventory should look like
:download:`this <../../examples/scenarios/monitoring_hosts/inventory.yaml>`:

.. literalinclude:: ../../examples/scenarios/monitoring_hosts/inventory.yaml
   :language: yaml

You probably noticed that we have a *subscriptions* variable defined for each
host. This host variable will allow us to use a single playbook to install
agents on different hosts with different configurations.

.. note::

   We are using a YAML inventory format in this document. Feel free to use any
   other Ansible-supported form if this one does not feel right to you.

Now we can move on and start preparing the playbook.


Preparing the playbook
----------------------

All we need to do in the playbook is to set some variables and call the
*sensu.sensu_go.agent* role. The initial version of the playbook would look
something like this:

.. code-block:: yaml

   ---
   - name: Install, configure and run Sensu agent
     hosts: agents
     become: true

     tasks:
       - name: Install agent
         include_role:
           name: sensu.sensu_go.agent

And while this playbook is fully functional as it is, we can make it a bit
safer by pinning down the version number. Another thing that we will do is to
replace the default configuration options for the agent with our own. After we
implement those changes, we end up with
:download:`this <../../examples/scenarios/monitoring_hosts/playbook.yaml>`:

.. literalinclude:: ../../examples/scenarios/monitoring_hosts/playbook.yaml
   :language: yaml

The *subscriptions* variable that we used in the *agent_config* comes from the
inventory and allows us to tweak the configuration of each agent
independently.

Another thing that the more observant of you might notice is the lack of any
information about the backend. We were able to omit it because we have a
backend group defined in the inventory. In cases like this, the agent role
knows how to construct the *backend-url* configuration option and
automatically insert it into the configuration.

We can override the default behavior by manually specifying the *backend-url*
configuration option in the *agent_config*. The agent role will stop being
smart in this case and use the value we provided.

And now, we are ready to execute the playbook.


Executing the playbook
----------------------

We are just one command away from having a fully-functioning monitoring setup
up and running. And the magic Ansible command is::

   $ ansible-playbook -i inventory.yaml playbook.yaml

If everything went according to plan, we should be able to see the two new
entities in the Sensu Go dashboard. We can now pat ourselves on the back and
call it a day ;)
