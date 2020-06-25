Managing Sensu Go Resources
===========================

Sensu Go Ansible collection contains quite a few modules for handling the
resources. But because they are doing their job by calling a web API instead
of directly manipulating the managed node, their use pattern is a bit
different from the regular Ansible module.

So let us start with a short introduction into how Ansible does its job.


Executing tasks
---------------

When we talk about Ansible, we usually assume that we have one **control
node** and one or more **managed nodes**. A control node is just fancy talk
for a system with Ansible installed. A managed node is usually a computer or a
virtual machine that Ansible connects to and modifies in one way or another.
We list our managed nodes in the inventory file and reference them using the
*hosts* playbook parameter.

When we execute the ``ansible-playbook`` command on the control node, Ansible
packages each task into a ball of python code (also called AnsiballZ), copies
the sources to the managed node, and executes them. This execution then
modifies the node and reports the changes back to the control node.

.. figure:: normal_execution.svg
   :alt: Diagram of a normal task execution.

   Diagram of a normal Ansible task execution.

But when modules are interacting with the web API, the node modification
process is replaced by the call to the external API. We must include all
parameters for this API call (like API host, credentials, etc.) in the task
definition. The managed node in this situation only serves as a temporary jump
host.

.. figure:: web_request_execution.svg
   :alt: Diagram of a web request task execution.

   Diagram of a web request task execution.

And while this kind of functionality is indeed required sometimes, most of the
time, we can make those web API calls directly from the control node. All we
need to do is set the *hosts* playbook parameter to ``localhost`` and drop the
inventory file since we do not need it anymore. Do note that Ansible is still
creating an AnsiballZ, but instead of copying it to the managed node, it just
makes a local copy on the control node.

.. figure:: web_request_localhost.svg
   :alt: Diagram of a web request task execution on localhost.

   Diagram of a web request task execution on localhost.

Now we can start managing resources for real.


Writing playbooks that manage resources
---------------------------------------

The most basic playbook for making sure ``sensu/monitoring-plugins`` asset is
present on the backend would look like this:

TODO: Add playbook for assets here.

Note that this playbook does not blindly add a new asset.

TODO: Explain idempotency.
TODO: Show using environment variables.
TODO: Show how to run the playbook.
