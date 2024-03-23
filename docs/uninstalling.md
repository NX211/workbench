# Uninstalling

**Warning**: If you have some trouble with your installation, you can just [re-run the playbook](installing.md) and it will try to set things up again. **Uninstalling and then installing anew rarely solves anything**.

To uninstall, run these commands (most are meant to be executed on the server itself):

- delete some cached Docker images (`docker system prune -a`) or just delete them all (`docker rmi $(docker images -aq)`)

- uninstall Docker itself, if necessary
