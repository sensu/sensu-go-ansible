Sensu Go Ansible Collection
===========================

Sensu Go `Ansible Collection`_ contains:

* Ansible role to install `Sensu Go`_ on your nodes.
* Ansible modules for interacting with `Sensu Go`_ REST API.

.. _Ansible Collection:
   https://docs.ansible.com/ansible/devel/user_guide/collections_using.html
.. _Sensu Go: https://docs.sensu.io/sensu-go/latest


Installation
------------

Just install the collection from Ansible Galaxy and you're good to go. If you
are using Ansible 2.9 or later, you can install Sensu Go collection by
running::

   $ ansible-galaxy collection install sensu.sensu_go

If you are using Ansible 2.8, you will need to install mazer_ first and then
run::

   $ mazer install sensu.sensu_go

.. _mazer: https://galaxy.ansible.com/docs/mazer/index.html

Older Ansible releases (< 2.8) do not support collections at all.


Usage
-----

You can use the namespaced modules::

   - hosts: localhost
     tasks:
       - name: List Assets
         sensu.sensu_go.asset_info:
         register: assets

       - name: List Filters
         sensu.sensu_go.filter_info:
         register: filters

Or add the collection to the search path and use bare names::

   - hosts: localhost
     collections: [sensu.sensu_go]
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
