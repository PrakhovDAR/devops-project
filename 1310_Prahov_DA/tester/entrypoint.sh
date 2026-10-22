#!/bin/bash

if [ -n "$SECOND_SSH_KEY" ]; then
    echo "$SECOND_SSH_KEY" >> /root/.ssh/authorized_keys
fi

#Запуск ssh с помощью daemon
/usr/sbin/sshd

exec python3 -m http.server 3000