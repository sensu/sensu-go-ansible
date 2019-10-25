Setting up a demo environment
=============================

To set up a simple Sensu Go sandbox, we just need the following playbook::

   ---
   - name: Install backend
     hosts: backends
     become: true

     tasks:
       - name: Install backend
         include_role:
           name: sensu.sensu_go.backend
         vars:
           backend_config:
             # Place your configuration here

   - name: Install agents
     hosts: agents
     become: true

     tasks:
       - name: Install agent
         include_role:
           name: sensu.sensu_go.agent
         vars:
           agent_config:
             # Place your configuration here

When we run it, it will install and configure backend and agents on selected
hosts. Note that we do not need to inform agents explicitly where the backend
is, because the role can deduce this on its own.

Now, before we can run this playbook, we need to prepare an inventory file.
The inventory should contain two groups of hosts: backends and agents. A
minimal inventory with only two hosts will look somewhat like this::

   all:
     vars:
       ansible_user: vagrant
       ansible_ssh_common_args: >
         -o IdentitiesOnly=yes
         -o BatchMode=yes
         -o UserKnownHostsFile=/dev/null
         -o StrictHostKeyChecking=no

     children:
       backends:
         hosts:
           192.168.50.4:

       agents:
         hosts:
           192.168.50.5:

You can safely ignore the ``ansible_ssh_common_args`` if you can reach your
hosts via ssh. We just left it there since this snippet comes in handy
sometimes.

All that we need to do now is to run the playbook::

   $ ansible-playbook -i inventory.yaml playbook.yaml

And in a few minutes, things should be ready to go.
