# Task Manager

## Описание проекта
Task Manager - это инструмент для управления задачами с возможностью отслеживания статуса, приоритета и сроков выполнения задач. Проект разработан с использованием [Python](https://www.python.org/) и [FastAPI](https://fastapi.tiangolo.com/).

## Особенности
- Выбор роли при регистрации
- Создание, редактирование и удаление задач (в зависимости от роли)
- Указание приоритета, статуса и сроков выполнения для каждой задачи
- Фильтрация и сортировка задач для удобного просмотра
- Аутентификация пользователей для сохранения и управления персональными задачами

## Установка и настройка

```shell
   git clone https://github.com/vebulogmetra/task_manageer.git
```
```shell
   cd task_manageer
```
```shell
   make d-build
```
```shell
   make d-start
```
```shell
   make d-stop
```

## Запуск тестов

```shell
   make d-run-tests
```

[Web UI](http://0.0.0.0:8000/front/pages/signup)
[API Docs](http://0.0.0.0:8000/docs)
