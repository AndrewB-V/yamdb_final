![Yamdb Workflow Status](https://github.com/andrewbond/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?branch=master&event=push)

# ЯП - Спринт 16 - CI и CD проекта api_yamdb. Python-разработчик (бекенд) (Яндекс.Практикум)

## Описание 

Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории:«Книги», «Фильмы», «Музыка». Список категорий  может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).
Настроика для приложения Continuous Integration и Continuous Deployment, реализация:
- автоматический запуск тестов,
- обновление образов на Docker Hub,
- автоматический деплой на боевой сервер при пуше в главную ветку main.

Стек:
- Django 2.2.28
- DRF 3.12.4
- djangorestframework-simplejwt 5.0.0


### Как запустить проект:
Все описанное ниже относится к ОС Linux.

### Клонируем репозиторий и и переходим в него:
```bash
git clone git@github.com:AndrewB-V/yamdb_final.git
```
```bash
cd yamdb_final
```
### Создаем и активируем виртуальное окружение:
```bash
python3 -m venv venv
```
- Windows:
```bash
source venv/Scripts/activate
```
- Linux:
```bash
source venv/bin/activate
```
### Обновим pip:
```bash
python -m pip install --upgrade pip 
```
### Установка зависимости из requirements.txt:
```bash
pip install -r api_yamdb/requirements.txt 
```
### Переходим в папку с файлом docker-compose.yaml:
```bash
cd infra
```
### Предварительно установим Docker на ПК под управлением Linux (Ubuntu 22.10), для Windows немного иная установка, тут не рассматриваем:
```bash
sudo apt update && apt upgrade -y
```
### Удаляем старый Docker:
```bash
sudo apt remove docker
```
### Устанавливаем Docker:
```bash
sudo apt install docker.io
```
### Смотрим версию Docker (должно выдать Docker version 20.10.16, build 20.10.16-0ubuntu1):
```bash
docker --version
```
### Активируем Docker в системе, что бы при перезагрузке запускался автоматом:
```bash
sudo systemctl enable docker
```
### Запускаем Docker:
```bash
sudo systemctl start docker
```
### Мониторинг статус:
```bash
sudo systemctl status docker
```
```bash
sudo docker run hello-world 
```
### Не будет лишнем установить PostgreSQL:
```bash
sudo apt -y install postgresql
```
### Предварительно в папке infra создаем файл .env с следующим содержимом:
```bash
DB_ENGINE=django.db.backends.postgresql 
DB_NAME=postgres 
POSTGRES_USER=postgres 
POSTGRES_PASSWORD=postgres 
DB_HOST=db 
DB_PORT=5432
```
### Поднимаем контейнеры (
###     infra_db - база,
###     infra_web - веб,
###     infra_nginx - nginx сервер
###     возможно пригодится команда sudo systemctl stop nginx если запускаете в DEV режиме на ПК):
```bash
sudo docker-compose up -d --build 
```
### Выполняем миграции в контейнере infra_web:
```bash
sudo docker-compose exec web python manage.py makemigrations reviews 
```
```bash
sudo docker-compose exec web python manage.py migrate --run-syncdb
```
### Создаем суперпользователя:
```bash
docker-compose exec web python manage.py createsuperuser 
```
### Собираем статику:
```bash
docker-compose exec web python manage.py collectstatic --no-input 
```
### Создаем дамп базы данных (нет в текущем репозитории):
```bash
docker-compose exec web python manage.py dumpdata > dumpPostrgeSQL.json 
```
### Останавливаем контейнеры:
```bash
docker-compose down -v 
```
### Документация API YaMDb 
Документация доступна по эндпойнту: http://localhost:8000/redoc/
### Автор: [AndrewBond](https://github.com/andrewbond) :+1: