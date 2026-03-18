# Todo List API

Лабораторная работа по Docker.
Приложение для управления задачами на Flask и PostgreSQL в Docker-контейнерах.

# Технологии

Python/Flask
PostgreSQL
Docker/Docker Compose
Nginx

# Запуск

docker-compose up -d --build

# Проверка

## Проверка здоровья
curl http://localhost:5000/health

## Получение всех задач
curl http://localhost:5000/api/tasks

## Получение задачи по ID
curl http://localhost:5000/api/tasks/1

# POST/PUT/DELETE запросы

## Создание новой задачи
$task = @{
    title = "Новая задача"
    priority = "high"
    description = "Описание задачи"
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:5000/api/tasks `
  -Method POST `
  -Body $task `
  -ContentType "application/json"

## Обновление задачи (отметить как выполненную)
$update = @{
    status = "completed"
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:5000/api/tasks/1 `
  -Method PUT `
  -Body $update `
  -ContentType "application/json"

## Удаление задачи
Invoke-RestMethod -Uri http://localhost:5000/api/tasks/2 `
  -Method DELETE
