Role sensu.sensu_go.install
=========

Install Sensu Go commands (`sensuctl`, `sensu-backend`, `sensu-agent`) from official
precompiled packages.

NOTE: This role only configures your package manager (like yum or apt) and installs
the binaries. It does **not** configure anything and it does **not** run any services.


Requirements
------------

This role has no requirements.

Role Variables
--------------

This role expects you to provide only a single variable, `components: []`, which is a list
of one or more Sensu Go components that you want to have installed in your inventory.
By default, all three components will be installed:

```yaml
components:
  - sensu-go-backend
  - sensu-go-agent
  - sensu-go-cli
```

You can specify exact version per component like this:

```yaml
components:
  - name: sensu-go-backend
    version: 5.12.0
  - name: sensu-go-cli
    version: 5.12.0
```

Supported Tags
---------

| Tag               | Effect                                                   |
|-------------------|----------------------------------------------------------|
| configure_install | Skip this tag to skip the package manager configuration; just install components |
| install           | Skip this tag to skip all tasks of the role; useful when role is required by other role but you don't want it to run 

Dependencies
------------

This role has not dependencies on other roles.

Example Playbook
----------------

```yaml
- name: Install sensu-backend and sensuctl binaries
  hosts: backends
  collections: [sensu.sensu_go]
  roles:
     - {role: install, components: [sensu-go-backend, sensu-go-cli]}

- name: Install sensu-agent binary
  hosts: agents
  collections: [sensu.sensu_go]
  roles:
     - {role: install, components: [sensu-go-agent]}

- name: Install sensuctl at specific version
  hosts: all
  collections: [sensu.sensu_go]
  roles:
     - role: install
       components:
          - {name: sensu-go-cli, version: '5.12.0'}
```

Tested Platforms (CI/CD)
------------------------
| OS       | Distributions                     |
|----------|-----------------------------------|
| Centos   | 6, 7                              |
| Ubuntu   | 14.04, 16.04, 18.04, 18.10, 19.04 |

License
-------

GPL3

Author Information
------------------

steampunk@xlab.si
