#!/bin/bash

# Настройка логирования: дублирование stdout и stderr
exec 3>&1 4>&2
exec 1> >(tee -a /opt/project/logs/stdout.log >&3)
exec 2> >(tee -a /opt/project/logs/stderr.log >&4)

echo "[INFO] Starting testing pipeline..."

RUN_YAPF=0
RUN_PYLINT=0
RUN_INTEGRATION=0

# Проверка переменной TEST_STAGES
if [ -z "$TEST_STAGES" ]; then
    RUN_YAPF=1; RUN_PYLINT=1; RUN_INTEGRATION=1
else
    if [[ "$TEST_STAGES" == *"yapf"* ]]; then RUN_YAPF=1; fi
    if [[ "$TEST_STAGES" == *"pylint"* ]]; then RUN_PYLINT=1; fi
    if [[ "$TEST_STAGES" == *"integration"* ]]; then RUN_INTEGRATION=1; fi
fi

if [ "$RUN_YAPF" -eq 1 ]; then
    echo "[STAGE] YAPF formatting check..."
    yapf --diff bad_code.py || echo "YAPF done."
fi

if [ "$RUN_PYLINT" -eq 1 ]; then
    echo "[STAGE] Pylint analysis..."
    pylint --disable=all \
           --enable=missing-module-docstring,missing-class-docstring,missing-function-docstring,invalid-name,unused-import,unused-variable,no-member,pointless-string-statement,undefined-variable,pointless-statement \
           bad_code.py || echo "Pylint done."
fi

if [ "$RUN_INTEGRATION" -eq 1 ]; then
    echo "[STAGE] Integration tests..."
    python3 test_integration.py
fi

echo "[INFO] Pipeline finished."