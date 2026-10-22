## Сборка и запуск контейнеров
**_Примечание_**: здесь и далее предполагается, что выполнение представленных команд производится из директории `1310_Prahov_DA`.
```sh
docker-compose up -d --build
```
## Запуск автоматизированных тестов
```sh
docker-compose exec tester /bin/bash -c "/tester/run.sh"
```
Команда выполняет следующие тесты:
- проверка на соответствие стилю кодирования (yapf);
- статический анализ по 10 критериям (pylint);
- интеграционные тесты кодов возврата.
Логи тестирования выводятся:
```sh
docker-compose logs tester
```
## Подключение по SSH
- контейнер `app`:
```sh
ssh -p 2222 -i ./ssh_keys/app_rsa root@localhost
```
- контейнер `tester`:
```sh
ssh -p 3333 -i ./ssh_keys/tester_rsa root@localhost
```
## Запуск тестов
#Только yapf:
```sh
docker-compose exec tester bash -c "python3 -c 'from tests.code_style import CodeStyle; CodeStyle().run_test()' >>/proc/1/fd/1 2>>/proc/1/fd/2"
```
#Только Pylint:
```sh
docker-compose exec tester bash -c "python3 -c 'from tests.static_analys import StaticAnalys; StaticAnalys().run_test()' >>/proc/1/fd/1 2>>/proc/1/fd/2"
```
#Только интеграционные тесты:
```sh
docker-compose exec tester bash -c "python3 -c 'from tests.integration import IntegrationTests; IntegrationTests().run_all_tests()' >>/proc/1/fd/1 2>>/proc/1/fd/2"
```