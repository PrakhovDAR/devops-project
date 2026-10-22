#!/bin/bash

# Запуск тестов
exec python3 main.py >>/proc/1/fd/1 2>>/proc/1/fd/2