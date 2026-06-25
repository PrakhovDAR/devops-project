#!/bin/bash
ssh-keygen -A
/usr/sbin/sshd
cd /EXAMPLE_APP
exec python3 main.py