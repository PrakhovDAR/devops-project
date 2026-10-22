#!/bin/bash

if [ -n "$SECOND_SSH_KEY" ]; then
    echo "$SECOND_SSH_KEY" >> /root/.ssh/authorized_keys
fi

patch /app/main.py <<EOF
52c52
<     return redirect(url_for('increment_int', a=a+1))
---
>     return str(a + 1)
EOF
patch /app/main.py <<EOF
78c78
<     app.run(debug = True)
---
>     app.run(debug=True, host='0.0.0.0')
EOF

#Запуск ssh с помощью daemon
/usr/sbin/sshd

exec python3 main.py