Role sensu.sensu_go.backend
=========

This role installs, configures and starts the Sensu Backend as a service.

Requirements
------------

This role has no requirements.

Role Variables
--------------

The role uses the `backend_config` top-level variable to populate the Sensu
backend's `/etc/sensu/backend.yml`configuration file as is documented in the
[official Sensu documentation][backend-conf]. The following `backend_config.*`
variables can be used in the playbooks:

| Variable    | Examples  | Description |
|-------------|-----------|-------------|
| debug       | false     | Enable debugging and profiling features |
| log-level   | panic/fatal/error/*warn*/info/debug | Logging level: `panic`, `fatal`, `error`, `warn`, `info`, or `debug` |
| agent-host  | "[::]"    | agent listener host, listens on all IPv4 and IPv6 addresses by default |
| agent-port  | 8081      | agent listener port |
| deregistration-handler | /path/to/handler.sh | Default event handler to use when processing agent deregistration events |
| api-listen-address | "[::]:8080" | Address the API daemon will listen for requests on |
| api-url     | "http://localhost:8080" | URL used to connect to the API |
| dashboard-host | "[::]"    | Dashboard listener host |
| dashboard-port | 3000      | Dashboard listener port |
| etcd-advertise-client-urls | "http://localhost:2379" |
| etcd-cert-file | "/path/to/ssl/cert.pem" | List of this member's client URLs to advertise to the rest of the cluster. |
| etcd-client-cert-auth | false | Path to the etcd client API TLS cert file. Secures communication between the embedded etcd client API and any etcd clients. |
| etcd-initial-advertise-peer-urls | "http://127.0.0.1:2380" | List of this member's peer URLs to advertise to the rest of the cluster |
| etcd-initial-cluster | "default=http://127.0.0.1:2380" | Initial cluster configuration for bootstrapping |
| etcd-initial-cluster-state | new/existing | Initial cluster state (`new` or `existing`) |
| etcd-initial-cluster-token | "sensu" | Initial cluster token for the etcd cluster during bootstrap |
| etcd-key-file | "/path/to/ssl/key.pem" | Path to the etcd client API TLS key file. Secures communication between the embedded etcd client API and any etcd clients |
| etcd-listen-client-urls | "http://127.0.0.1:2379" | List of URLs to listen on for client traffic |
| etcd-listen-peer-urls | "http://127.0.0.1:2380" | List of URLs to listen on for peer traffic |
| etcd-name | "default" | Human-readable name for this member |
| etcd-peer-cert-file | "/path/to/ssl/cert.pem" | Path to the peer server TLS cert file |
| etcd-peer-client-cert-auth | false | Enable peer client cert authentication |
| etcd-peer-key-file | "/path/to/ssl/key.pem" | Path to the etcd peer API TLS key file. Secures communication between etcd cluster members |
| etcd-peer-trusted-ca-file | "/path/to/ssl/key.pem" | Path to the etcd peer API server TLS trusted CA file. This certificate secures communication between etcd cluster members |
| etcd-trusted-ca-file | "/path/to/ssl/key.pem" | Path to the client server TLS trusted CA cert file. Secures communication with the etcd client server |
| no-embed-etcd | false | Don't embed etcd, use external etcd instead |
| etcd-cipher-suites | [] | List of allowed cipher suites for etcd TLS configuration. Sensu supports TLS 1.0-1.2 cipher suites as listed in the [Go TLS documentation][]. You can use this attribute to defend your TLS servers from attacks on weak TLS ciphers. The default cipher suites are determined by Go, based on the hardware used. |


All of the `backend_config` variables are optional, so when we omit them from
the role, the Sensu backend will use a version-specific default.
The role automatically sets the following `backend_config` variables, so
assigning custom values to them might have unexpected results:

* `state-dir`

[backend-conf]: https://docs.sensu.io/sensu-go/latest/reference/backend/#configuration-summary
[Go TLS documentation]: https://golang.org/pkg/crypto/tls/#pkg-constants


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
