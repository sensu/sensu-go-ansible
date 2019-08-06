# Sensu Go Ansible Modules

This [Ansible Collection][] contains:

- Ansible role to install [Sensu Go][] on your nodes
- Ansible modules for interacting with [Sensu Go][] REST API

[Ansible Collection]: https://docs.ansible.com/ansible/devel/dev_guide/collections_tech_preview.html
[Sensu Go]: https://docs.sensu.io/sensu-go/latest

## Installation
Just install the collection from Ansible Galaxy and you're good to go:

```
ansible-galaxy collection install sensu.sensu_go
```

## Usage

You can use the namespaced modules:
```
- hosts: localhost
  tasks:
    - name: List Assets
      sensu.sensu_go.sensu_go_asset_info:
      register: assets

    - name: List Filters
      sensu.sensu_go.sensu_go_filter_info:
      register: filters
```

Or add the collection to the search path and use bare names:

```
- hosts: localhost
  collections: [sensu.sensu_go]
  tasks:
    - name: List Assets
      sensu_go_asset_info:
      register: assets

    - name: List Filters
      sensu_go_filter_info:
      register: filters
```

## Acknowledgement
We would like to thank [@flowerysong](https://github.com/flowerysong/ansible-sensu-go) for
initial implementation of the Ansible modules provided in this collection.
