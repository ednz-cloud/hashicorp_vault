Hashicorp Nomad
=========
> This repository is only a mirror. Development and testing is done on a private gitlab server.

This role install and configure nomad on **debian-based** distributions.

Requirements
------------

None.

Role Variables
--------------
Available variables are listed below, along with default values. A sample file for the default values is available in `default/hashicorp_nomad.yml.sample` in case you need it for any `group_vars` or `host_vars` configuration.

```yaml
hashi_nomad_install: true # by default, set to true
```
This variable defines if the consul package is to be installed or not before configuring. If you install consul using another task, you can set this to `false`.

```yaml
hashi_nomad_start_service: true
```
This variable defines if the nomad service should be started once it has been configured. This is usefull in case you're using this role to build golden images, in which case you might want to only enable the service, to have it start on the next boot (when the image is launched)

```yaml
hashi_nomad_version: latest # by default, set to latest
```
This variable specifies the version of nomad to install when `hashi_nomad_install` is set to `true`. The version to specify is the version of the package on the hashicorp repository (`1.5.1-1` for example).

```yaml
hashi_nomad_deploy_method: host # by default, set to host
```
This variable defines the method of deployment of nomad. The `host` method installs the binary directly on the host, and runs nomad as a systemd service. The `docker` method install nomad as a docker container.
> Currently, only the `host` method is available, the `docker` method will be added later.

```yaml
hashi_nomad_server_enabled: true # by default, set to true
hashi_nomad_client_enabled: false # by default, set to false
hashi_nomad_acl_enabled: false # by default, set to false
```
These variables enable or disable the server, client and acl functions for nomad.

```yaml
hashi_nomad_server:
```
This variable sets a bunch of configuration parameters for nomad. For more information on all of them, please check the [documentation](https://developer.hashicorp.com/nomad/docs/configuration). I try to name them the same as in the configuration file, so that it is easier to search for it. Most of the defaults in the role are the default values of nomad, however, some might differ.

```yaml
hashi_nomad_consul_enabled: false # by default, set to false
hashi_nomad_consul:
```
This variable sets up the consul integration for nomad, to use for networking, service catalog, and kv storage.`hashi_nomad_consul` contains the configuration in case you enable it.

```yaml
hashi_nomad_vault_enabled: false # by default, set to false
hashi_nomad_vault:
```
This variable sets up the vault integration for nomad, to use for secrets storage. `hashi_nomad_vault` contains the configuration in case you enable it.

```yaml
hashi_nomad_docker_driver_enabled: false # by default, set to false
hashi_nomad_docker_driver:
```
This variable enables the docker plugin for nomad. Note that the role DOES NOT install docker. You might use a dedicated role for this. Enabling this assumes that docker is already running on the host. `hashi_nomad_docker_driver` contains the configuration in case you enable it.

Dependencies
------------

This role requires both `ednxzu.manage_repositories` and `ednxzu.manage_apt_packages` to install nomad. If you already installed nomad, you can set `hashi_nomad_install` to `false`, and that'll remove the dependencies.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:
```yaml
# calling the role inside a playbook with either the default or group_vars/host_vars
- hosts: servers
  roles:
    - ednxzu.hashicorp_nomad
```

License
-------

MIT / BSD

Author Information
------------------

This role was created by Bertrand Lanson in 2023.
