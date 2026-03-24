# Обувной магазин (shoes_shop)

[![Maintainability](https://qlty.sh/gh/oayaivaivb/projects/shoes_shop/maintainability.svg)](https://qlty.sh/gh/oayaivaivb/projects/shoes_shop)

Система учёта товаров и заказов для магазина обуви. Реализована на Django с разграничением ролей (гость, авторизованный клиент, менеджер, администратор).

## Функциональность

- **Гость** – просмотр каталога товаров.
- **Авторизованный клиент** – просмотр каталога.
- **Менеджер** – просмотр товаров с поиском, фильтром по поставщику, сортировкой по остатку; просмотр заказов.
- **Администратор** – полное управление товарами (CRUD, загрузка изображений) и заказами (CRUD).

## Технологии

- Django 5.1+
- Bootstrap 5 (через `django-bootstrap5`)
- SQLite (по умолчанию)
- Pillow (обработка изображений)

## Установка и запуск

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/ваш-логин/shoes_shop.git
   cd shoes_shop
   ```

2. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Примените миграции:
   ```bash
   python manage.py migrate
   ```

5. Создайте суперпользователя (администратора):
   ```bash
   python manage.py createsuperuser
   ```

6. Запустите сервер разработки:
   ```bash
   python manage.py runserver
   ```

7. Перейдите на [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Данные для входа

В базе уже есть тестовые пользователи (пароли из файла `Копия user_import.csv`):

| Логин (email)              | Пароль  | Роль         |
|----------------------------|---------|--------------|
| 94d5ous@gmail.com          | uzWC67  | администратор |
| 1diph5e@tutanota.com       | 8ntwUp  | менеджер      |
| 5d4zbu@tutanota.com        | rwVDh9  | клиент        |

> Чтобы войти как гость, нажмите соответствующую кнопку на странице входа.

## Структура проекта

```
shoes_shop/
├── shoes/                # основное приложение
├── shoes_shop/           # настройки Django
├── templates/            # шаблоны HTML
├── static/               # CSS, изображения, иконки
├── manage.py
├── requirements.txt
└── README.md
```
