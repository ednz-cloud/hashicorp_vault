"""Role testing files using testinfra."""
import json


def test_hosts_file(host):
    """Validate /etc/hosts file."""
    etc_hosts = host.file("/etc/hosts")
    assert etc_hosts.exists
    assert etc_hosts.user == "root"
    assert etc_hosts.group == "root"

def test_vault_user_group(host):
    """Validate vault user and group."""
    vault_group = host.group("vault")
    vault_user = host.user("vault")
    assert vault_group.exists
    assert vault_user.exists
    assert vault_user.group == "vault"
    assert vault_user.shell == "/bin/false"

def test_vault_config(host):
    """Validate /etc/vault.d/ files."""
    etc_vault_d_vault_env = host.file("/etc/vault.d/vault.env")
    etc_vault_d_vault_json = host.file("/etc/vault.d/vault.json")
    for file in etc_vault_d_vault_env, etc_vault_d_vault_json:
        assert file.exists
        assert file.user == "vault"
        assert file.group == "vault"
        assert file.mode == 0o600
        if file == etc_vault_d_vault_json:
            assert file.content_string != ""

def test_vault_storage(host):
    """Validate /opt/vault directory."""
    opt_vault = host.file("/opt/vault")
    assert opt_vault.exists
    assert opt_vault.is_directory
    assert opt_vault.user == "vault"
    assert opt_vault.group =="vault"
    assert opt_vault.mode == 0o755

def test_vault_service_file(host):
    """Validate vault service file."""
    lib_systemd_system_vault_service = host.file("/etc/systemd/system/vault.service")
    assert lib_systemd_system_vault_service.exists
    assert lib_systemd_system_vault_service.user == "root"
    assert lib_systemd_system_vault_service.group == "root"
    assert lib_systemd_system_vault_service.mode == 0o644
    assert lib_systemd_system_vault_service.content_string != ""

def test_vault_service(host):
    """Validate vault service."""
    vault_service = host.service("vault.service")
    assert vault_service.is_enabled
    assert vault_service.is_running
    assert vault_service.systemd_properties["Restart"] == "on-failure"
    assert vault_service.systemd_properties["User"] == "vault"
    assert vault_service.systemd_properties["Group"] == "vault"
    assert vault_service.systemd_properties["EnvironmentFiles"] == "/etc/vault.d/vault.env (ignore_errors=yes)"
    assert vault_service.systemd_properties["FragmentPath"] == "/etc/systemd/system/vault.service"

def test_vault_interaction(host):
    """Validate interaction with vault."""
    vault_operator_init = host.check_output("VAULT_ADDR=http://localhost:8200 vault operator init -non-interactive -key-shares=3 -key-threshold=2 -tls-skip-verify -format=json")
    vault_operator_init = json.loads(vault_operator_init)
    vault_unseal_keys = vault_operator_init['unseal_keys_hex']
    vault_token = vault_operator_init['root_token']
    vault_unseal_0 = host.check_output("VAULT_ADDR=http://localhost:8200 vault operator unseal -format=json -tls-skip-verify " + vault_unseal_keys[0])
    vault_unseal_0 = json.loads(vault_unseal_0)
    vault_unseal_1 = host.check_output("VAULT_ADDR=http://localhost:8200 vault operator unseal -format=json -tls-skip-verify " + vault_unseal_keys[1])
    vault_unseal_1 = json.loads(vault_unseal_1)
    assert vault_unseal_0['sealed']
    assert not vault_unseal_1['sealed']
    vault_kv_mount = host.check_output("VAULT_ADDR=http://localhost:8200 VAULT_TOKEN=" + vault_token + " vault secrets enable -version=1 -tls-skip-verify kv")
    assert vault_kv_mount == "Success! Enabled the kv secrets engine at: kv/"
