Role sensu.sensu_go.agent
=========

This role installs, configures and starts the Sensu Agent as a service.

Requirements
------------

This role has no requirements.

Role Variables
--------------

Most variables are directly interpolated into the /etc/sensu/agent.yml configuration file
which is documented in the [official Sensu documentation][agent-conf]. Please refer to it to
learn what exactly each specific parameter does.

| Variable            | Default Value | Description |
|---------------------|---------------|-------------|
| agent_backends      | /             | see [Sensu docs][agent-conf]
| agent_log_level     | /             | see [Sensu docs][agent-conf]

[backend-conf]: https://docs.sensu.io/sensu-go/latest/reference/agent/#configuration-summary


Supported Tags
---------

| Tag               | Effect                                                   |
|-------------------|----------------------------------------------------------|
| install           | Use `--skip-tags install` to skip the installation and go straight to the configuration. 
| configure_agent   | Use `--tags configure_agent` to just configure agent without running it.  
| run_agent         | Use `--tags run_agent` to just run the agent as a service.  

Dependencies
------------

This role depends on role `sensu.sensu_go.install` which is part of this same collection.
The role is used to install sensu-agent binary to the system.

Example Playbook
----------------

```yaml
- name: Install, configure and run Sensu agent
  hosts: backends
  collections: [sensu.sensu_go]
  roles:
     - role: agent
       agent_backend_urls: ['ws://upstream-backend:4321']
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
