#!/bin/bash

# Set defaults for PUID and PGID if not specified
PUID=${PUID:-1000}
PGID=${PGID:-1000}

# Remove the user and group if they exist
echo "Attempting to delete existing user and group..."
userdel m3uuser >/dev/null 2>&1
groupdel m3ugroup >/dev/null 2>&1

# Create the group
echo "Creating new group 'm3ugroup'..."
groupadd -g "$PGID" m3ugroup

# Create the user
echo "Creating new user 'm3uuser'..."
useradd -u "$PUID" -g "$PGID" --no-log-init m3uuser

# Set ownership and permissions
echo "Setting ownership and permissions..."
chown -R "$PUID:$PGID" /usr/src/app
chmod +x /usr/src/app/hours.sh

# Switch to the m3uuser and run hours.sh
echo "Switching to user 'm3uuser' and running hours.sh..."
su -s /bin/bash -c "exec /usr/src/app/hours.sh" m3uuser

# Exit the entrypoint script
echo "Entrypoint script execution completed."
exit 0

