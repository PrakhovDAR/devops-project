# Вариант 7

Проект демонстрирует выполнение задания по Docker и Docker Compose:

- проверка HTML через `html-linter`;
- статический анализ Python через `pylint` по 10 включенным критериям;
- интеграционный тест загрузки файла через `requests`;
- SSH-доступ в `app` и `tester` по существующему публичному ключу;
- вывод каждого этапа тестирования в `docker logs`, а также в общие файлы `logs/stdout.log` и `logs/stderr.log`;
- передача публичного SSH-ключа и параметров тестирования через `.env`;
- ограничение ОЗУ каждого контейнера до `170m`.

## Запуск

```bash
cp .env.example .env
docker-compose build
docker-compose up
```

По умолчанию SSH доступен только на localhost:

- `app`: `127.0.0.1:2222`;
- `tester`: `127.0.0.1:2223`.

## Параметры `.env`

- `PUBLIC_SSH_KEY` - публичный ключ для доступа в оба контейнера.
- `APP_SSH_PORT` - порт SSH для контейнера `app`.
- `TESTER_SSH_PORT` - порт SSH для контейнера `tester`.
- `APP_MEMORY_LIMIT` - лимит ОЗУ для `app`, по варианту 7 это `170m`.
- `TESTER_MEMORY_LIMIT` - лимит ОЗУ для `tester`, по варианту 7 это `170m`.
- `TEST_STAGES` - список этапов тестирования: `html,pylint,integration`.
- `UPLOAD_FILE_NAME` - имя файла для интеграционного теста загрузки.

## Проверка логов

```bash
docker-compose logs tester
cat logs/stdout.log
cat logs/stderr.log
```
