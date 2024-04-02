hashicorp_vault
=========
> This repository is only a mirror. Development and testing is done on a private gitea server.

This role install and configure vault on **debian-based** distributions.

Requirements
------------

None.

Role Variables
--------------
Available variables are listed below, along with default values.

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
hashi_vault_extra_files_list: [] # by default, set to []
  # - src: /tmp/directory
  #   dest: /etc/vault.d/directory
  # - src: /tmp/file.conf
  #   dest: /etc/vault.d/file.conf
  # - src: /etc/vault.d/file.j2
  #   dest: /etc/vault.d/file
```
This variable lets you copy extra configuration files and directories over to the target host(s). It is a list of dicts. Each dict needs a `src` and a `dest` attribute. The source is expected to be located on the deployment machine. The source can be either a file or a directory. The destination must match the type of the source (file to file, dir to dir). If the source is a directory, every file inside of it will be recursively copied and templated over to the target directory.

For example, if you have the following source files to copy:

```bash
├── directory
│   ├── recursive
│   │   ├── test4.j2
│   │   └── test.j2024.conf
│   └── test3
├── file
├── file2.j2
```
You can set:

```yaml
hashi_vault_extra_files_list: [] # by default, set to []
  - src: /tmp/directory
    dest: /etc/vault.d/directory
  - src: /tmp/file
    dest: /etc/vault.d/file.conf
  - src: /etc/vault.d/file2.j2
    dest: /etc/vault.d/file2.conf
```
all the files shown above will be copied over, and the directory structure inside `directory` will be preserved.

> **Note**
> In case you're using the `docker` deployment method, every destination path will be added automatically to the `hashi_vault_extra_container_volumes` variable, so you don't need to set them manually.


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

`ednz_cloud.manage_repositories` to configure the hashicorp apt repository.
`ednz_cloud.docker_systemd_service` if installing vault in a container.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:
```yaml
# calling the role inside a playbook with either the default or group_vars/host_vars
- hosts: servers
  roles:
    - ednz_cloud.hashicorp_vault
```

License
-------

MIT / BSD

Author Information
------------------

This role was created by Bertrand Lanson in 2023.
