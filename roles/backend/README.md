Role sensu.sensu_go.backend
=========

This role installs, configures and starts the Sensu Backend as a service.

Requirements
------------

This role has no requirements.

Role Variables
--------------

Most variables are directly interpolated into the /etc/sensu/backend.yml configuration file
which is documented in the [official Sensu documentation][backend-conf]. Please refer to it to
learn what exactly each specific parameter does.

| Variable            | Default Value | Description |
|---------------------|---------------|-------------|
| backend_debug       | /             | see [Sensu docs][backend-conf]
| backend_log_level   | /             | see [Sensu docs][backend-conf]

[backend-conf]: https://docs.sensu.io/sensu-go/latest/reference/backend/#configuration-summary


Supported Tags
---------

| Tag               | Effect                                                   |
|-------------------|----------------------------------------------------------|
| install           | Use `--skip-tags install` to skip the installation and go straight to the configuration. 
| configure_backend | Use `--tags configure_backend` to just configure backend without running it.  
| run_backend       | Use `--tags run_backend` to just run the backend as a service.  

Dependencies
------------

This role depends on role `sensu.sensu_go.install` which is part of this same collection.
The role is used to install sensu-backend binary to the system.

Example Playbook
----------------

```yaml
- name: Install, configure and run Sensu backend
  hosts: backends
  collections: [sensu.sensu_go]
  roles:
     - backend

- name: Install, configure and run Sensu backend in debug mode
  hosts: backends
  collections: [sensu.sensu_go]
  roles:
     - role: backend
       backend_debug: yes
       backend_log_level: debug
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
