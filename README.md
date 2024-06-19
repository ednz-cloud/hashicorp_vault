hashicorp_vault
=========
![Ansible Badge](https://img.shields.io/badge/Ansible-E00?logo=ansible&logoColor=fff&style=for-the-badge)
![HashiCorp Badge](https://img.shields.io/badge/HashiCorp-000?logo=hashicorp&logoColor=fff&style=for-the-badge)
![Vault Badge](https://img.shields.io/badge/Vault-FFEC6E?logo=vault&logoColor=000&style=for-the-badge)

> This repository is only a mirror. Development and testing is done on a private gitea server.

This role install and configure vault on **debian-based** distributions.

Requirements
------------

The `unzip` package needs to be installed on the target host(s) to be able to decompress the consul release bundle.

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
This variable specifies the version of vault to install. The version to specify is either `latest` (NOT RECOMMENDED), or any tag present on the [GitHub Repository](https://github.com/hashicorp/vault/releases) (without the leading `v`). Loose tags are **not supported** (1.7, 1, etc..).

```yaml
hashi_vault_env_variables: # by default, set to {}
  ENV_VAR: value
```
This value is a list of key/value that will populate the `vault.env` file.

```yaml
hashi_vault_data_dir: "/opt/vault" # by default, set to /opt/vault
```
This value defines the path where vault data will be stored on the node. Defaults to `/opt/vault`.

```yaml
hashi_vault_extra_files: false # by default, set to false
```
This variable defines whether or not there is extra configuration files to copy to the target.

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

```yaml
hashi_vault_configuration: {} # by default, set to a simple configuration
```
This variable sets all of the configuration parameters for vault. For more information on all of them, please check the [documentation](https://developer.hashicorp.com/vault/docs/configuration). This variable is parsed and converted to json format to create the config file, so each key and value should be set according to the documentation. This method of passing configuration allows for compatibility with every configuration parameters that vault has to offer. The defaults are simply here to deploy a simple, single-node vault server without much configuration, and should NOT be used in production. You will want to edit this to deploy production-ready clusters.

Dependencies
------------

None.

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
