#!/bin/bash
set -e

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

# ── Configure SSH authorised keys ──────────────────────────────────────────
log "=== Configuring SSH ==="
mkdir -p /root/.ssh
chmod 700 /root/.ssh
touch /root/.ssh/authorized_keys
chmod 600 /root/.ssh/authorized_keys

if [ -n "${SSH_PUBLIC_KEY}" ]; then
    printf '%s\n' "${SSH_PUBLIC_KEY}" > /root/.ssh/authorized_keys
    log "SSH public key written to authorized_keys"
else
    log "WARNING: SSH_PUBLIC_KEY is not set. Key-based SSH login will not work."
fi

# ── Start SSH daemon in the background ────────────────────────────────────
mkdir -p /var/run/sshd
log "Starting SSH daemon..."
/usr/sbin/sshd

# ── Start Flask application as PID 1 ──────────────────────────────────────
log "=== Starting Flask application ==="
cd /app
export FLASK_APP=main.py && exec flask run --host=0.0.0.0 --port=5000
