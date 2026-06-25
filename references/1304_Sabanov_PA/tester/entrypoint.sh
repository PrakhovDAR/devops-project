#!/bin/bash
set -euo pipefail

TESTER_SSH_USER=tester
TESTER_SSH_PASSWORD="${TESTER_SSH_PASSWORD:-changeme}"

if ! id "${TESTER_SSH_USER}" >/dev/null 2>&1; then
	useradd --create-home --shell /bin/bash "${TESTER_SSH_USER}"
fi

echo "${TESTER_SSH_USER}:${TESTER_SSH_PASSWORD}" | chpasswd

if [ ! -f /etc/ssh/ssh_host_rsa_key ]; then
	ssh-keygen -A
fi

mkdir -p /run/sshd
cat > /etc/ssh/sshd_config <<EOF
Port 22
PasswordAuthentication yes
UsePAM no
PidFile /run/sshd.pid
EOF

/usr/sbin/sshd

exec "$@"