#!/bin/sh
set -eu

if [ -n "${PUBLIC_SSH_KEY:-}" ]; then
  mkdir -p /home/devops/.ssh
  printf '%s\n' "$PUBLIC_SSH_KEY" > /home/devops/.ssh/authorized_keys
  chown -R devops:devops /home/devops/.ssh
  chmod 700 /home/devops/.ssh
  chmod 600 /home/devops/.ssh/authorized_keys
fi

mkdir -p /opt/tester/logs
touch "${LOG_STDOUT:-/opt/tester/logs/stdout.log}" "${LOG_STDERR:-/opt/tester/logs/stderr.log}"
chown -R devops:devops /opt/tester/logs
chmod 775 /opt/tester/logs
chmod 664 "${LOG_STDOUT:-/opt/tester/logs/stdout.log}" "${LOG_STDERR:-/opt/tester/logs/stderr.log}"
: > "${LOG_STDOUT:-/opt/tester/logs/stdout.log}"
: > "${LOG_STDERR:-/opt/tester/logs/stderr.log}"

/usr/sbin/sshd
exec su -s /bin/sh devops -c "python3 /opt/project/tester/run_tests.py"
