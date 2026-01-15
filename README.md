# MediaRadar — Веб-сервис уведомлений о релизах медиа-контента

![Python](https://img.shields.io/badge/python-3.10+-blue)
![Django](https://img.shields.io/badge/django-6.0+-darkgreen)

**Веб-приложение для подписки на медиа-контент с автоматическими уведомлениями о новых эпизодах через Email.**

---

## 📝 Описание

**MediaRadar** — это веб-сервис для занятых людей, которые хотят получать уведомления о выходе новых эпизодов своих любимых сериалов.

Вместо того чтобы постоянно проверять сайты, пользователи подписываются на интересующие их сериалы один раз, и затем автоматически получают уведомления на электронную почту или в Telegram при выходе нового эпизода.

**Цель проекта:** упростить процесс отслеживания релизов медиа-контента и сэкономить время пользователей.

---

## ✨ Основные возможности

### Для пользователей

- 🔍 **Поиск сериалов** — интеграция с API TVMaze для поиска в реальном времени
- 📺 **Подписка на сериалы** — управление списком отслеживаемых шоу
- 🔔 **Уведомления** — получение оповещений о новых эпизодах на Email
- 📜 **Подписки** — просмотр всех активных подписок

### Для администраторов

- ⚙️ **Django Admin Panel** — управление всеми сущностями (Title, Release, Subscription, NotificationLog)
- 📊 **Фильтрация и поиск** — быстрый поиск по названиям и источникам
- 📋 **История уведомлений** — отслеживание статуса отправленных уведомлений

---

## 🛠 Технологический стек

### Backend

| Компонент | Технология |
|-----------|-----------|
| Язык | Python 3.10+ |
| Фреймворк | Django 6.0 |
| ORM | Django ORM |
| БД | SQLite3 |
| HTTP-клиент | requests |
| Email | SMTP (Gmail) |
| Логирование | Python logging |

### Frontend

| Компонент | Технология |
|-----------|-----------|
| Шаблонизация | Django Templates |
| CSS | Custom CSS |

### Инструменты и сервисы

| Инструмент | Назначение |
|-----------|-----------|
| Git | Контроль версий |
| pip | Менеджер пакетов Python |
| TVMaze API | Источник данных о сериалах |

---

## 📦 Требования

- **Python:** 3.10 или выше
- **pip:** для установки зависимостей
- **Git:** для клонирования репозитория
- **Email:** Gmail аккаунт с app-password (для отправки уведомлений)
- **Интернет:** для подключения к TVMaze API

---

## 🚀 Установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/Armontex/media-radar.git
```

### 2. Создание виртуального окружения

**Linux/MacOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Создание каптчи

1. [Быстрый старт по созданию YandexSmartCaptcha](https://yandex.cloud/ru/docs/smartcaptcha/quickstart)

### 5. Создание бота

1. [Создать Telegram-bot](https://core.telegram.org/bots#3-how-do-i-create-a-bot)

### 6. Создание файла .env (опционально)

```bash
# .env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_SENDER=your-email@gmail.com
EMAIL_APP_PASSWORD=your-app-password
CAPTCHA_SERVER_KEY=your-captcha-server-key
CAPTCHA_CLIENT_KEY=your-captcha-client-key
BOT_TOKEN=your-bot-token
```

### 7. Миграции БД

```bash
python manage.py migrate
```

### 8. Создание суперпользователя (администратора)

```bash
python manage.py createsuperuser
```

---

## ▶️ Запуск

### Локальная разработка

```bash
python manage.py runserver
```

Приложение будет доступно по адресу: `http://127.0.0.1:8000`

**Для доступа в админ-панель:**

`http://127.0.0.1:8000/admin`

---

## 📂 Структура проекта (# FIXME: Исправить)

```tree
.
├── apps
│   ├── core
│   │   ├── config.py
│   │   ├── constants.py
│   │   ├── exc.py
│   │   └── logger.py
│   ├── __init__.py
│   ├── mailers
│   │   ├── constants.py
│   │   ├── __init__.py
│   │   ├── smtp.py
│   │   ├── templates
│   │   │   └── notify.html
│   │   └── utils.py
│   ├── providers
│   │   ├── base.py
│   │   ├── enums.py
│   │   ├── __init__.py
│   │   ├── mappers.py
│   │   ├── schemas.py
│   │   ├── tvmaze.py
│   │   └── utils.py
│   └── utils
│       ├── http.py
│       └── __init__.py
├── config
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── y.py
├── db.sqlite3
├── .env
├── .gitignore
├── manage.py
├── radar
│   ├── admin.py
│   ├── apps.py
│   ├── choices.py
│   ├── forms.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_profile_remove_notificationlog_user_and_more.py
│   │   └── __init__.py
│   ├── models.py
│   ├── static
│   │   └── radar
│   │       ├── icons
│   │       │   ├── account_circle.svg
│   │       │   ├── add.svg
│   │       │   ├── delete.svg
│   │       │   └── subscriptions.svg
│   │       ├── scss
│   │       │   ├── base
│   │       │   │   ├── _base.scss
│   │       │   │   ├── _fonts.scss
│   │       │   │   ├── _reset.scss
│   │       │   │   └── _vars.scss
│   │       │   ├── components
│   │       │   │   ├── _catalog.scss
│   │       │   │   ├── _footer.scss
│   │       │   │   ├── _form_wrapper.scss
│   │       │   │   ├── _header.scss
│   │       │   │   └── _inputform.scss
│   │       │   ├── home.scss
│   │       │   ├── layouts
│   │       │   │   └── _container.scss
│   │       │   ├── login.scss
│   │       │   ├── profile.scss
│   │       │   ├── register.scss
│   │       │   └── subscriptions.scss
│   │       └── styles
│   │           ├── home.css
│   │           ├── home.css.map
│   │           ├── login.css
│   │           ├── login.css.map
│   │           ├── profile.css
│   │           ├── profile.css.map
│   │           ├── register.css
│   │           ├── register.css.map
│   │           ├── subscriptions.css
│   │           └── subscriptions.css.map
│   ├── tasks.py
│   ├── templates
│   │   ├── radar
│   │   │   ├── base.html
│   │   │   ├── home.html
│   │   │   ├── not_found.html
│   │   │   ├── profile.html
│   │   │   └── subscriptions.html
│   │   └── registration
│   │       ├── login.html
│   │       └── register.html
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── README.md
├── requirements.txt
└── TZ.md
```

---

## 🌐 API и источники данных

### TVMaze API

**Источник:** https://www.tvmaze.com/api

#### Поиск сериалов
```
GET /search/shows?q=<query>
```

**Ответ:**
```json
[
  {
    "score": 12.5,
    "show": {
      "id": 1,
      "name": "Under the Dome",
      "image": {
        "medium": "https://...",
        "original": "https://..."
      }
    }
  }
]
```

#### Информация о сериале
```
GET /shows/<id>
```

**Ответ:**
```json
{
  "id": 1,
  "name": "Under the Dome",
  "summary": "<p>...</p>",
  "image": {
    "medium": "https://...",
    "original": "https://..."
  }
}
```

#### Эпизоды сериала
```
GET /shows/<id>/episodes
```

**Ответ:**
```json
[
  {
    "id": 1,
    "season": 1,
    "number": 1,
    "name": "Pilot",
    "airdate": "2013-06-24"
  }
]
```

---

## 💻 Использование

### Регистрация нового пользователя

1. Перейдите на http://localhost:8000/account/register
2. Введите username и пароль
3. Указать email при регистрации
4. Нажмите "Зарегистрироваться"

### Поиск и подписка на сериал

1. Перейдите на главную страницу (/)
2. В поле "Поиск" введите название сериала (например, "Сваты")
3. Из результатов выберите нужный сериал
4. Нажмите "Добавить в подписки" (Плюсик)
5. Подписка создана!

### Просмотр подписок

1. Перейдите на страницу подписок (/subscriptions)
2. Здесь видны все ваши активные подписки
3. Для удаления нажмите кнопку "Удалить"

### Профиль

1. Профиль (/profile)

---

## 👨‍💻 Разработка

### Создание новой миграции

После изменения моделей:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🔒 Безопасность

### Перед продакшеном:

- [ ] Установить `DEBUG = False`
- [ ] Изменить `SECRET_KEY` на случайную строку
- [ ] Установить `ALLOWED_HOSTS` с вашим доменом
- [ ] Настроить HTTPS (включен по умолчанию на PythonAnywhere)
- [ ] Изменить дефолтный пароль администратора
- [ ] Использовать переменные окружения для чувствительных данных
- [ ] Регулярно обновлять зависимости
- [ ] Включить CSRF protection (уже включена в Django)

---

## 🐛 Решение проблем

### Проблема: ImportError при запуске

**Решение:** Убедитесь что виртуальное окружение активировано:
```bash
source venv/bin/activate  # Linux/MacOS
```

### Проблема: "No module named django"

**Решение:** Переустановите зависимости:
```bash
pip install -r requirements.txt
```

### Проблема: Миграции не применяются

**Решение:** Выполните следующее:
```bash
python manage.py migrate
python manage.py makemigrations
python manage.py migrate
```

### Проблема: Email уведомления не отправляются

**Решение:**
1. Проверьте EMAIL_SENDER и EMAIL_APP_PASSWORD
2. Убедитесь что используется app-password для Gmail (не основной пароль)
3. Проверьте логи в `logs`

---

## 📚 Полезные ресурсы

### Документация

- [Django Документация](https://docs.djangoproject.com/en/6.0/)
- [Django ORM](https://docs.djangoproject.com/en/6.0/topics/db/models/)
- [Django Views](https://docs.djangoproject.com/en/6.0/topics/http/views/)
- [TVMaze API](https://www.tvmaze.com/api)

### Tools

- [Visual Studio Code](https://code.visualstudio.com/)

---

## 🎯 Автор

**Автор:** [Armontex](https://github.com/Armontex)
**Дата создания:** Январь 2026  
**Версия:** 1.0.0
