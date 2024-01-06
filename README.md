hashicorp_vault
=========
> This repository is only a mirror. Development and testing is done on a private gitea server.

This role install and configure vault on **debian-based** distributions.

Requirements
------------

None.

Role Variables
--------------
Available variables are listed below, along with default values. A sample file for the default values is available in `default/hashicorp_vault.yml.sample` in case you need it for any `group_vars` or `host_vars` configuration.

```yaml
hashi_vault_start_service: true
```
This variable defines if the vault service should be started once it has been configured. This is usefull in case you're using this role to build golden images, in which case you might want to only enable the service, to have it start on the next boot (when the image is launched)

```yaml
hashi_vault_version: latest # by default, set to latest
```
This variable specifies the version of vault to install when `hashi_vault_install` is set to `true`. The version to specify is the version of the package on the hashicorp repository (`1.10.1-1` for example). This can be found by running `apt-cache madison vault` on a machine with the repository installed.

If the version is set to `latest`, the role will update the package/docker image on every run if a newer version is available. This will cause a restart cycle of your node/cluster, to update every node to the latest version. Updating vault is usually pretty safe if done on a regular basis (given that you need a way to unseal the nodes upon restart), but for better control over the upgrade process, please set the variable to a static release version.

```yaml
hashi_vault_deploy_method: host # by default, set to host
```
This variable defines the method of deployment of vault. The `host` method installs the binary directly on the host, and runs vault as a systemd service. The `docker` method install vault as a docker container.
> Currently, only the `host` method is available, the `docker` method will be added later.

```yaml
hashi_vault_env_variables: # by default, set to {}
  ENV_VAR: value
```
This value is a list of key/value that will populate the `vault.env`(for host deployment method) or `/etc/default/vault`(for docker deploy method) file.

```yaml
hashi_vault_data_dir: "/opt/vault" # by default, set to /opt/vault
```
This value defines the path where vault data will be stored on the node. Defaults to `/opt/vault`.

```yaml
hashi_vault_extra_files: false # by default, set to false
```
This variable defines whether or not there is extra configuration files to copy to the target. If true, these files can be anything static (no jinja2 templates).

```yaml
hashi_vault_extra_files_src: /tmp/extra_files # by default, set to /tmp/extra_files
```
This variable defines the source directory (without the trailing /) for the extra files to be copied in case there are some. The entire directory structure above the defined directory will be copied recursively to the target host.

```yaml
hashi_vault_extra_files_dst: /etc/vault.d/extra_files # by default, set to /etc/vault.d/extra_files
```
This variable defines the destination directory (without the trailing /) for the extra files to be copied.

```yaml
hashi_vault_extra_container_volumes: [] # by default, set to []
```
This variable lets you defines more volumes to mount inside the container when using the `docker` deployment method. This is a list of string in the form: `"/path/on/host:/path/on/container"`. These volumes will not be created/checked before being mounted, so they need to exist prior to running this role.

```yaml
hashi_vault_configuration: {} # by default, set to a simple configuration
```
This variable sets all of the configuration parameters for vault. For more information on all of them, please check the [documentation](https://developer.hashicorp.com/vault/docs/configuration). This variable is parsed and converted to json format to create the config file, so each key and value should be set according to the documentation. This method of passing configuration allows for compatibility with every configuration parameters that vault has to offer. The defaults are simply here to deploy a simple, single-node vault server without much configuration, and should NOT be used in production. You will want to edit this to deploy production-ready clusters.

Dependencies
------------

`ednxzu.manage_repositories` to configure the hashicorp apt repository.
`ednxzu.docker_systemd_service` if installing vault in a container.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:
```yaml
# calling the role inside a playbook with either the default or group_vars/host_vars
- hosts: servers
  roles:
    - ednxzu.hashicorp_vault
```

License
-------

MIT / BSD

Author Information
------------------

This role was created by Bertrand Lanson in 2023.
