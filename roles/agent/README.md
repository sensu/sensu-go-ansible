Role sensu.sensu_go.agent
=========

This role installs, configures and starts the Sensu Agent as a service.

Requirements
------------

This role has no requirements.

Role Variables
--------------

The role uses the `agent_config` top-level variable to populate the Sensu
agent's `/etc/sensu/agent.yml`configuration file as is documented in the
[official Sensu documentation][agent-conf]. The following `agent_config.*`
variables can be used in the playbooks:

| Variable    | Examples  | Description |
|-------------|-----------|-------------|
| annotations | `sensu.io/plugins/slack/config/webhook-url: "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"`| Non-identifying metadata to include with event data, which can be accessed using filters and tokens. You can use annotations to add data that's meaningful to people or external tools interacting with Sensu. |
| backend-url | `["ws://0.0.0.0:8081", "ws://0.0.0.0:8082"]` | ws or wss URL of the Sensu backend server. *NOTE:* the role populates this variable from the play's inventory |
| cache-dir   | /cache/sensu-agent | Path to store cached data |
| disable-assets | false  | When set to true, disables assets for the agent. In the event that an agent attempts to execute a check that requires an asset, the agent will respond with a status of 3, and a message indicating that the agent could not execute the check because assets are disabled. |
| allow-list  | /etc/sensu/check-allow-list.yaml | Path to yaml or json file containing allowlist of check or hook commands the agent can execute. See the example configuration file and the configuration spec for details on building a configuration file. |
| label       | `proxy_type: "website"` | Custom attributes to include with event data, which can be accessed using filters and tokens |
| name        | agent-01  | Entity name assigned to the agent entity |
| log-level   | panic/fatal/error/*warn*/info/debug | Logging level: `panic`, `fatal`, `error`, `warn`, `info`, or `debug` |
| subscriptions | ['disk-checks', 'process-checks'] | An array of agent subscriptions which determine which monitoring checks are executed by the agent. The subscriptions array items must be strings |
| api-host    | 192.168.10.3 | An array of agent subscriptions which determine which monitoring checks are executed by the agent. The subscriptions array items must be strings |
| api-port    | 3031      | Listening port for the Sensu agent HTTP API |
| events-burst-limit | 10 | The maximum amount of burst allowed in a rate interval for the agent events API |
| events-rate-limit: | 10.0 | The maximum number of events per second that can be transmitted to the backend using the agent events API |
| deregister  | false     | Indicates whether a deregistration event should be created upon Sensu agent process stop |
| deregistration-handler | deregister | The name of a deregistration handler that processes agent deregistration events. This flag overrides any handlers applied by the `deregistration-handler` backend configuration flag |
| keepalive-interval | 20 | Number of seconds between keepalive events|
| keepalive-timeout | 120 | Number of seconds after a missing keepalive event until the agent is considered unresponsive by the Sensu backend |
| namespace   | ops       | Agent namespace. *NOTE*: Agents are represented in the backend as a class of entity. Entities can only belong to a single namespace |
| user        | agent-01  | Sensu RBAC username used by the agent. Agents require get, list, create, update, and delete permissions for events across all namespaces |
| password    | P@ssw0rd! | Sensu RBAC password used by the agent |
| redact      | ['secret', 'ec2_access_key'] | List of fields to redact when displaying the entity |
| trusted-ca-file | /path/to/trusted-certificate-authorities.pem | SSL/TLS certificate authority |
| insecure-skip-tls-verify | false | Skip SSL verification |
| socket-host | 127.0.0.1 | Address to bind the Sensu agent socket to |
| socket-port | 1303      | Port the Sensu agent socket listens on |
| disable-sockets | false | Disable the agent TCP and UDP event sockets |
| statsd-disable | false  | Disables the StatsD listener and metrics server |
| statsd-event-handlers | ['influxdb', 'opentsdb'] | List of event handlers for StatsD metrics |
| statsd-flush-interval | 10 | Number of seconds between StatsD flush |
| statsd-metrics-host | 127.0.0.1 | Address used for the StatsD metrics server |
| statsd-metrics-port | 8125 | Port used for the StatsD metrics server |
| exec        | /usr/local/bin/check_memory.sh | The command to allow the Sensu agent to run as a check or a hook |
| sha512      | 34736924c7902c7e6df902 ... | The checksum of the check or hook executable |
| args        | ["foo"] | The checksum of the check or hook executable |
| enable_env  | true    | Enable environment variables |

[agent-conf]: https://docs.sensu.io/sensu-go/latest/reference/agent/#configuration-summary


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
