Quickstart for Sensu Go 6
=========================

Before we can do anything, we need to install Sensu Go Ansible Collection.
Luckily, we are just one short command away from that goal::

   $ ansible-galaxy collection install sensu.sensu_go

Now we can set up a simple Sensu Go sandbox using the following
:download:`playbook <../examples/quickstart/playbook-6.yaml>`:

.. literalinclude:: ../examples/quickstart/playbook-6.yaml
   :language: yaml

When we run it, Ansible will install and configure backend and agents on
selected hosts, and then configure a ntp check that agents will execute twice
a minute. Note that we do not need to inform agents explicitly where the
backend is because the :doc:`agent role <roles/agent>` can obtain the
backend's address from the inventory.

Now, before we can run this playbook, we need to prepare an inventory file.
The inventory should contain two groups of hosts: *backends* and *agents*. A
:download:`minimal inventory <../examples/quickstart/inventory.yaml>` with
only two hosts will look somewhat like this:

.. literalinclude:: ../examples/quickstart/inventory.yaml
   :language: yaml

Replace the IP addresses with your own and make sure you can ssh into those
hosts. If you need help with building your inventory file, consult `official
documentation on inventory`_.

.. _official documentation on inventory:
   https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html

All that we need to do now is to run the playbook::

   $ ansible-playbook -i inventory.yaml playbook-6.yaml

And in a few minutes, things should be ready to go. And if we now visit
http://192.168.50.4:3000 (replace that IP address with the address of your
backend), we can log in and start exploring.
