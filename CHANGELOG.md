## v0.3.0 (2024-07-19)

### Feat

- change variables to ease integration in hashistack collection while remaining usable as a standalone role
- replaces variables to better integrate with hashistack collection while remaining usable as a standalone role

## v0.2.1 (2024-07-12)

### Fix

- check if vault service is not in a failed state to trigger restart if needed

## v0.2.0 (2024-06-19)

### Feat

- change variables naming convention to conform to ansible-lint policy

## v0.1.0 (2024-06-19)

### Feat

- change deployment method, deprecate docker deployment, adjust tests,documentation and variable accordingly
- new cicd flow, cz and pre-commits, remove vagrant tests
- **extra_files**: ensure destination directory exists before copying
- **defaults**: remove old extra_files defaults
- **extra_files**: allow copying multiple extra_files sources, either files or directories, recursvively, and allow jinja2 templating inside of them
- **core**: change namespace
- **readme**: update readme for extra_files
- **task/configure**: copy entire directory structure, does not deal with templates anymore
- **docker**: use /etc/vault.d as config dir in docker container instead of the default
- **readme**: update readme to reflect changes in variables
- **task**: remove old references to ednxzu.install_apt_packages role
- **task**: remove dependency for installing vault from repo, ensure rolling restart on multiple hosts
- **task**: add option to mount extra volumes to container
- **test**: some experiementation with raft storage on containers
- **tests**: change with_raft_enabled_vagrant to use docker deploy method
- **tests**: make default_vagrant tests use docker deploy method
- **tasks**: add install_docker tasks, revamp variables to accomodate
- remove become from role
- add vagrant tests, add become, fix #1

### Fix

- do not attempt to loop over non-existant variable if no extra files or no extra dirs
