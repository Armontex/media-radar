# MediaRadar
<!-- Badges -->
![Python](https://img.shields.io/badge/python-3.12+-blue)
![Django](https://img.shields.io/badge/django-6.0-darkgreen)
![Docker](https://img.shields.io/badge/docker-blue)

---

## Содержание

- [MediaRadar](#mediaradar)
  - [Содержание](#содержание)
  - [Описание](#описание)
  - [Запуск и установка LINUX (DEV)](#запуск-и-установка-linux-dev)
    - [Важные дополнения](#важные-дополнения)
      - [Получение ключей, токенов и паролей](#получение-ключей-токенов-и-паролей)
        - [EMAIL\_APP\_PASSWORD](#email_app_password)
        - [SECRET\_KEY](#secret_key)
        - [CAPTCHA\_SERVER\_KEY и CAPTCHA\_CLIENT\_KEY](#captcha_server_key-и-captcha_client_key)
        - [BOT\_TOKEN](#bot_token)
      - [Получение SITE\_HOST через LocalTunnel](#получение-site_host-через-localtunnel)
      - [Авторизация через Telegram](#авторизация-через-telegram)
  - [Запуск и установка (Docker)](#запуск-и-установка-docker)
  - [Использование](#использование)
    - [Регистрация нового пользователя](#регистрация-нового-пользователя)
    - [Авторизация](#авторизация)
    - [Профиль](#профиль)
    - [Поиск и подписка на сериал](#поиск-и-подписка-на-сериал)
    - [Просмотр подписок](#просмотр-подписок)
    - [Примеры уведомлений](#примеры-уведомлений)
      - [Email](#email)
      - [Telegram](#telegram)
  - [API и Данные](#api-и-данные)
    - [TVMaze API (поиск сериалов)](#tvmaze-api-поиск-сериалов)
    - [TelegramBot API (отправка уведомлений)](#telegrambot-api-отправка-уведомлений)
    - [Gmail SMTP (отправка уведомлений)](#gmail-smtp-отправка-уведомлений)
  - [Лицензия](#лицензия)

---

## Описание

**MediaRadar** — это веб-сервис для занятых людей, которые хотят получать уведомления о выходе новых эпизодов своих любимых сериалов.

Вместо того чтобы постоянно проверять сайты, пользователи подписываются на интересующие их сериалы один раз, и затем автоматически получают уведомления на электронную почту или в Telegram при выходе нового эпизода.

**Цель проекта:** упростить процесс отслеживания релизов медиа-контента и сэкономить время пользователей.

![home](/docs/images/home.png)

---

## Запуск и установка LINUX (DEV)

**Требования**: Перед установкой у вас должен быть установлен python 3.12+ и pip 24.0+.

1. Клонирование репозитория

```bash
git clone https://github.com/Armontex/media-radar.git
```

2. Переход в директорию media-radar

```bash
cd media-radar
```

3. Создание виртуального окружения

```bash
python3 -m venv .venv
```

4. Активация виртуального окружения

```bash
source .venv/bin/activate
```

5. Установка зависимостей

```bash
pip install -r requirements.txt
```

6. Создание `.env`

```bash
touch .env
```

7. Заполнение `.env`

```env
EMAIL_APP_PASSWORD=your-app-password
EMAIL_SENDER=your-email
SECRET_KEY=your-django-secret-key
DEBUG=True
DATABASE_URL=sqlite:///data/db.sqlite3
SITE_HOST=example.com

CAPTCHA_SERVER_KEY=your-yandex-smart-captcha-server-key
CAPTCHA_CLIENT_KEY=your-yandex-smart-captcha-client-key
BOT_TOKEN=your-telegram-bot-token
```

Чтобы заполнить ключи, читаем [Важные дополнения](#важные-дополнения).

8. Миграции БД

```bash
python manage.py migrate
```

9. Создание супер-пользователя

```bash
python manage.py createsuperuser
```

10. Запуск

```bash
python manage.py runserver
```

**Приложение будет доступно по адресу**: `http://127.0.0.1:8000`

**Для доступа в админ-панель:** `http://127.0.0.1:8000/admin`

### Важные дополнения

#### Получение ключей, токенов и паролей

##### EMAIL_APP_PASSWORD

Настройка зависит от используемого почтового провайдера.

- [Gmail](https://support.google.com/mail/answer/185833?hl=ru)

##### SECRET_KEY

```bash
python manage.py shell
```

```python
from django.core.management.utils import get_random_secret_key
get_random_secret_key()
```

##### CAPTCHA_SERVER_KEY и CAPTCHA_CLIENT_KEY

[Как начать работать с Yandex SmartCaptcha](https://yandex.cloud/ru/docs/smartcaptcha/quickstart)

[Получение ключей](https://yandex.cloud/ru/docs/smartcaptcha/quickstart#get-keys)

Ключ сервера = CAPTCHA_SERVER_KEY
Ключ клиента = CAPTCHA_CLIENT_KEY

##### BOT_TOKEN

[Как создать бота в Telegram](https://core.telegram.org/bots#how-do-i-create-a-bot)

#### Получение SITE_HOST через LocalTunnel

[Быстрый старт LocalTunnel](https://localtunnel.github.io/www/)

Когда пропишите все команды, получите:

```plain
your url is: https://{some-text}.loca.lt
```

SITE_HOST={some-text}.loca.lt

*Примечание*:

1. Чтобы поставить свой subdomain (вместо some-text своё, к примеру, mediaradar)

```bash
lt --port 8000 --subdomain mediaradar
```

2. Если LocalTunnel не пускает и требует пароль, переходим на сайт `https://loca.lt/mytunnelpassword` *(Главное, чтобы ip, с которого запускаете `lt --port ...` совпадал с ip с которого заходите по ссылке)*. Паролем будет ip-адрес.

#### Авторизация через Telegram

1. Переходите в [@BotFather](https://t.me/botfather)

2. Вводите команду `/setdomain`

3. Выбираете бота, которого создали в [BOT_TOKEN](#bot_token)

4. Вводите SITE_HOST

---

## Запуск и установка (Docker)

1. Клонирование репозитория

```bash
git clone https://github.com/Armontex/media-radar.git
```

2. Переход в директорию media-radar

```bash
cd media-radar
```

3. Создание `.env`

```bash
touch .env
```

4. Заполнение `.env`

```env
EMAIL_APP_PASSWORD=your-app-password
EMAIL_SENDER=your-email
SECRET_KEY=your-django-secret-key
DEBUG=True
DATABASE_URL=sqlite:///{path_to_database}/db.sqlite3
SITE_HOST=example.com

CAPTCHA_SERVER_KEY=your-yandex-smart-captcha-server-key
CAPTCHA_CLIENT_KEY=your-yandex-smart-captcha-client-key
BOT_TOKEN=your-telegram-bot-token
```

Чтобы заполнить ключи, читаем [Важные дополнения](#важные-дополнения).

5. Создаём db.sqlite3

```bash
mkdir data
touch data/db.sqlite3
```

6. Создаём образ и запускаем

```bash
docker compose up -d
```

7. Миграции БД и супер-пользователь

```bash
docker compose exec media-radar python manage.py migrate
docker compose exec -it media-radar python manage.py createsuperuser
```

8. Рестарт (по необходимости)

```bash
docker compose restart
```

---

## Использование

### Регистрация нового пользователя

![register](/docs/images/auth_register.png)

Вариант 1:



1. Перейдите на `/auth/register`
2. Введите username и пароль
3. Указать email при регистрации
4. Пройдите captcha
5. Нажмите "Создать аккаунт"

Вариант 2 (Если есть SITE_HOST):

1. Перейдите на `https://SITE_HOST/auth/register/`
2. Нажмите "Войти через телеграм"

Вариант 3 (Если есть SITE_HOST):

1. Перейдите на `https://SITE_HOST/auth/`
2. Нажмите "Войти через телеграм"

### Авторизация

![login](/docs/images/auth_login.png)

Вариант 1:

1. Перейдите на `/auth/`
2. Введите username и пароль
3. Нажмите "Войти"

Вариант 2 (Если есть SITE_HOST):

1. Перейдите на `https://SITE_HOST/auth/register/`
2. Нажмите "Войти через телеграм"

### Профиль

Вариант 1 (Если регистрировались через username и пароль):

![profile-not-tg](/docs/images/profile_not-tg.png)

1. Перейдите на `/profile/`
2. Есть возможность привязать Telegram-аккаунт, который ранее не был привязан.
3. Если Telegram успешно привяжется, будет возможность выбора канала уведомлений.

Вариант 2 (Если регистрировались через Telegram):

![profile-1](/docs/images/profile.png)

1. Перейдите на `https://SITE_HOST/profile/`
2. Есть возмозность добавить почту, для этого введите почту и нажмите "Сохранить"
3. Если почта привязалась без ошибок, то появится возможность выбора канала уведомлений

Для обоих вариантов:

4. Есть возможность выйти из аккаунта, нажав на кнопку "Выйти"

![profile-2](/docs/images/profile_2.png)

### Поиск и подписка на сериал

![search_results_with_login](/docs/images/search_results_with_login.png)

1. Перейдите на главную страницу (/)
2. В поле "Поиск" введите название сериала (например, "Simpsons")
3. Из результатов выберите нужный сериал
4. Нажмите на плюсик.
5. Подписка добавлена!

### Просмотр подписок

![subscriptions](/docs/images/subscriptions.png)

1. Перейдите на страницу подписок (/subscriptions)
2. Здесь видны все ваши активные подписки
3. Для удаления нажмите корзину

### Примеры уведомлений

#### Email
![notify-example-email](/docs/images/notify_example_email.png)

#### Telegram

![notify-example-tg](/docs/images/notify_example_telegram.png)

---

## API и Данные

### TVMaze API (поиск сериалов)

**Источник**: https://www.tvmaze.com/api

### TelegramBot API (отправка уведомлений)

**Источник**: https://core.telegram.org/bots/api

### Gmail SMTP (отправка уведомлений)

---

## Лицензия

[LICENSE](./LICENSE)
