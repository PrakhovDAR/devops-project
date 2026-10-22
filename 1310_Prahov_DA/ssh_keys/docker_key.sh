#!/bin/bash

# 1) Генерация SSH-ключа для docker_app
'if [ ! -f app_rsa ]; then
    echo "Docker_app rsa key"
    ssh-keygen -t rsa -b 4096 -f app_rsa -N ""
else
    echo "Docker_app rsa key already exists"
fi
'
if [ ! -f tester_rsa ]; then
    echo "Docker_tester rsa key"
    ssh-keygen -t rsa -b 4096 -f tester_rsa -N ""
else
    echo "Docker_tester rsa key already exists"
fi

'if [ ! -f env_rsa ]; then
    echo "For env rsa key"
    ssh-keygen -t rsa -b 4096 -f env_rsa -N ""
else
    echo "For env rsa key already exists"
fi
'
chmod 600 app_rsa tester_rsa env_rsa