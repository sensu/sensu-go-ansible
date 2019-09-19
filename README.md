# Sensu Go Ansible Modules

This [Ansible Collection][] contains:

  * Ansible role to install [Sensu Go][] on your nodes
  * Ansible modules for interacting with [Sensu Go][] REST API

   [Ansible Collection]: https://docs.ansible.com/ansible/devel/dev_guide/collections_tech_preview.html
                         (Ansible documentation on collections)
   [Sensu Go]: https://docs.sensu.io/sensu-go/latest
               (Sensu Go documentation)


## Installation

Just install the collection from Ansible Galaxy and you're good to go:

    ansible-galaxy collection install -p ~/.ansible/collections sensu.sensu_go


## Usage

You can use the namespaced modules:

    - hosts: localhost
      tasks:
        - name: List Assets
          sensu.sensu_go.asset_info:
          register: assets

        - name: List Filters
          sensu.sensu_go.filter_info:
          register: filters

Or add the collection to the search path and use bare names:

    - hosts: localhost
      collections: [sensu.sensu_go]
      tasks:
        - name: List Assets
          asset_info:
          register: assets

        - name: List Filters
          filter_info:
          register: filters


## Support

Sensu will offer support for the contents of the collection. Details about the
support will be made available as soon as the collection is certified.


## Acknowledgement

We would like to thank [@flowerysong][flowerysong] for initial implementation
of the Ansible modules provided in this collection.

   [flowerysong]: https://github.com/flowerysong/ansible-sensu-go
                  (Original collection repo)
