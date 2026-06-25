#!/bin/sh
set -eu

if [ -n "${PUBLIC_SSH_KEY:-}" ]; then
  mkdir -p /home/devops/.ssh
  printf '%s\n' "$PUBLIC_SSH_KEY" > /home/devops/.ssh/authorized_keys
  chown -R devops:devops /home/devops/.ssh
  chmod 700 /home/devops/.ssh
  chmod 600 /home/devops/.ssh/authorized_keys
fi

/usr/sbin/sshd
exec su -s /bin/sh devops -c "python3 /opt/app/app.py"
