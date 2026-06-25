# Курсовая работа по ТАПРПО
**Вариант 36**

## Контейнеры
- app - контейнер с веб-приложением (Flask)
- tester - контейнер с тестами и SSH-доступом

> [!NOTE]
> В проекте используется новая версия Docker Compose, которая вызывается командой `docker compose` (с пробелом), в отличие от старой версии, которая вызывается командой `docker-compose` (с дефисом).

## Подготовка
```bash
cp .env.example .env # отредактируйте .env при необходимости
docker compose build
docker compose up -d # или без -d при запуске в отдельном терминале
```

## Запуск тестов
### Запуск тестов как обычных программ
```bash
docker compose exec tester python3 /opt/project/scripts/run_pipeline.py
```

Можно запустить отдельные этапы:
```bash
docker compose exec tester python3 /opt/project/scripts/test_yapf.py
docker compose exec tester python3 /opt/project/scripts/test_pylint.py
docker compose exec tester python3 /opt/project/scripts/test_headers.py
```

### Запуск тестов как тестов unittest
```bash
docker compose exec tester python3 -m unittest discover /opt/project/scripts/
```

Можно запустить отдельные тесты:
```bash
docker compose exec -w /opt/project/scripts tester python3 -m unittest test_yapf.py
docker compose exec -w /opt/project/scripts tester python3 -m unittest test_pylint.py
docker compose exec -w /opt/project/scripts tester python3 -m unittest test_headers.py
```

## SSH-доступ в tester
```bash
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null tester@127.0.0.1 -p 2222
```
Пароль из `.env` (`.env.example`) (переменная `TESTER_SSH_PASSWORD`).

В команде указаны флаги:
- `-o StrictHostKeyChecking=no` для ускорения процесса входа (не спрашивает подтверждение);
- `-o UserKnownHostsFile=/dev/null` для избежания добавления хоста в постоянное хранилище.

Эти флаги необязательны.

## Просмотр логов
Логи тестов с timestamp доступны через команду:
```bash
docker compose logs tester
```