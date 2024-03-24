# grist-uffd

Process to import users from uffd into [Grist](https://www.getgrist.com) and grant them access.

We use the [forwarded auth](https://support.getgrist.com/install/forwarded-headers/) mechanism with Grist but it seems
that new users are added with no permissions (and invites via email don't work). This process imports the user list from
uffd and adds them to the group defined by `GRIST_GROUP_ID`.


## Environment variables
```
UFFD_API_ENDPOINT="https://identity.example.org"
UFFD_API_USER="<API user>"
UFFD_API_PASSWORD="<API pass>"

GRIST_DB_PATH="/persistent/home.sqlite3"
GRIST_GROUP_ID="20"
```