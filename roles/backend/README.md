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
| state-dir   | /var/lib/sensu/sensu-backend | Path to Sensu state storage. Default value: `/var/lib/sensu/sensu-backend`. |
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

[backend-conf]: https://docs.sensu.io/sensu-go/latest/reference/backend/#configuration-summary
[Go TLS documentation]: https://golang.org/pkg/crypto/tls/#pkg-constants

Securing Sensu Go backend
-------------------------

This role enables users to establish secure end-to-end communications of
the components that comprise the Sensu Go backend. The user needs to supply the
paths to the PKI files by placing the appropriate public and private key files
somewhere within the Ansible playbook search path. They then need to reference
these paths in the appropriate inventory variables, as described below.

Note: all the files referenced in each of the following subsections need to be
supplied. If even a single file is missing or not defined, the play will fail.
If none of the variables within a subsection is defined, those services will
be configured without the secure communication.

## Etcd peer communication

To secure the etcd communication, create the appropriate files for the PKI
and define **all** of the following variables:

| Variable    | Examples  | Description |
|-------------|-----------|-------------|
| etcd_cert_file | files/pki/etcd-client.crt | Path to the certificate used for SSL/TLS connections **to** etcd. This is a client certificate. |
| etcd_key_file | files/pki/etcd-client.key | Path to the private key for the etcd client certificate file. Must be unencrypted. |
| etcd_trusted_ca_file | files/pki/client-ca.crt | Path to the trusted certificate authority for the etcd client certificates. |
| etcd_peer_cert_file | files/pki/etcd-peer.crt | Path to the certificate used for SSL/TLS connections between peers. This will be used both for listening on the peer address as well as sending requests to other peers. |
| etcd_peer_key_file | files/pki/etcd-peer.key | Path to the peer certificate's key. Must be unencrypted. |
| etcd_peer_trusted_ca_file | files/pki/etcd-peer-ca.crt | Pat to the trusted certificate authority for the peer certificates. |

## Backend API

To secure the Sensu Go backend API communication, create the appropriate files
for the PKI and define **all** of the following variables:

| api_cert_file | files/pki/sensu-api.crt | Path to the certificate used to secure the Sensu Go API. |
| api_key_file | files/pki/sensu-api.key | Path to the private key corresponding to the Sensu Go API certificate. Must be unencrypted. |
| api_trusted_ca_file | files/pki/sensu-api-ca.crt | Path to the trusted certificate authority for the Sensu Go API certificates. |

## Dashboard

To secure the dashboard communication, create the appropriate files for the PKI
and define **all** of the following variables:

| dashboard_cert_file | files/pki/sensu-dashboard.crt | Path to the certificate used for SSL/TLS connections to the dashboard. |
| dashboard_key_file | files/pki/sensu-dashboard.key | Path to the private key corresponding to the dashboard certificate. Must be unencrypted. |

The role will automatically configure the dashboard endpoint to use HTTPS,
e.g.: `https://localhost:3000`.



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
