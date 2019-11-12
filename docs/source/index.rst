Sensu Go Ansible Collection
===========================

Sensu Go `Ansible Collection`_ contains:

* Ansible roles to install `Sensu Go`_ on your nodes.
* Ansible modules for interacting with `Sensu Go`_ REST API.

.. _Ansible Collection:
   https://docs.ansible.com/ansible/latest/user_guide/collections_using.html
.. _Sensu Go: https://docs.sensu.io/sensu-go/latest


Installation
------------

If we would like to install the Sensu Go collection, we need to have Ansible
2.9 or later installed. Once we have taken care of this, we can install the
Sensu Go collection from `Ansible Galaxy`_ by running::

   $ ansible-galaxy collection install sensu.sensu_go

.. _Ansible Galaxy: https://galaxy.ansible.com


Usage
-----

We can use the namespaced modules::

   - hosts: localhost
     roles:
       - sensu.sensu_go.backend
     tasks:
       - name: List Assets
         sensu.sensu_go.asset_info:
         register: assets

       - name: List Filters
         sensu.sensu_go.filter_info:
         register: filters

Or use the `collections` keyword to create the search path, then use bare
names::

   - hosts: localhost
     collections: [sensu.sensu_go]
     roles:
       - backend
     tasks:
       - name: List Assets
         asset_info:
         register: assets

       - name: List Filters
         filter_info:
         register: filters


Support
-------

Sensu will offer support for the contents of the collection. Details about the
support will be made available as soon as the collection is certified.


Acknowledgement
---------------

We would like to thank `@flowerysong`_ for initial implementation of the
Ansible modules provided in this collection.

.. _@flowerysong: https://github.com/flowerysong/ansible-sensu-go


.. toctree::
   :maxdepth: 1
   :hidden:

   sandbox
   module_index
