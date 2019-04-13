# Sensu Go Ansible Modules

This [Ansible](https://www.ansible.com/) Collection implements a number of
modules for interacting with [Sensu Go](https://sensu.io/).

## Installation

Ansible Collections were added as a technology preview in Ansible 2.8,
and are a new method of distributing namespaced Ansible components
that are not integrated into the core source tree.

They can be installed into a playbook-adjacent `collections`
directory, `~/.ansible/collections`, or the system-wide
`/usr/share/ansible/collections`, or you can modify Ansible's
configuration to specify custom locations.

Clone this repo into whichever location strikes your fancy as
`collections/ansible_collections/flowerysong/sensu_go`

### Why a Collection?

In-tree modules introduce a certain amount of overhead to every
step of the development process, inevitably increase the workload
on core developers even with ansibot's workflow automation and
multiple active module maintainers, and tie new modules and bugfixes
to Ansible's release schedule. Publishing a Collection allows me to
make these modules publicly available with minimal extra work.

## Usage

You can use the namespaced modules:
```
- name: Disable Tessen
  flowerysong.sensu_go.sensu_go_tessen:
    enabled: false
    password: dead60ff
```

Or add the collection to the search path and use bare names:

```
- collections:
    - flowerysong.sensu_go
  module_defaults:
    group/sensu_go:
      password: dead60ff
  block:
    - name: Bind admins to the admin role
      sensu_go_rolebinding:
        name: blackops-admin
        cluster: true
        role: cluster-admin
        groups:
          - blackops

    - name: Monitor vault
      sensu_go_check:
        name: vault
        command: check-vault-status
        subscriptions:
          - Class_vault
```

Custom `module_defaults` groups are not supported in vanilla Ansible
2.8, but the patch that enables them will hopefully be upstreamed in
2.9.
