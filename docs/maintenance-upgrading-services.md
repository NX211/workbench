# Upgrading services

This playbook not only installs various services for you, but can also upgrade them as new versions are made available.

To upgrade services:

- update your playbook directory (`git pull`), so you'd obtain everything new we've done

- take a look at [the changelog](../CHANGELOG.md) to see if there have been any backward-incompatible changes that you need to take care of

- download the upstream Ansible roles used by the playbook by running `just roles`

- re-run the [playbook setup](installing.md) and restart all services: `just setup-all`
