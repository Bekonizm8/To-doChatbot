# 📝 To-DoChatbot — To-Do Manager with Telegram Bot

## 📖 Описание проекта

**To-doChatbot** — это система управления задачами, которая объединяет веб-интерфейс и Telegram-бота. Пользователи могут создавать, редактировать и отслеживать задачи как через браузер, так и прямо из Telegram. Веб-панель отображает аналитику в реальном времени: количество пользователей, общее число задач, выполненные и незавершённые. Telegram-бот позволяет управлять задачами через команды — устанавливать приоритеты, дедлайны, искать и отмечать задачи выполненными.

---

## 🛠 Используемые технологии

| Категория | Технология |
|---|---|
| Backend | Python 3.11+, Django 4+ |
| Telegram Bot | python-telegram-bot 20+ |
| База данных | SQLite (по умолчанию) / PostgreSQL |
| Frontend | HTML5, CSS3 (Django Templates) |
| Асинхронность | asyncio, asgiref |
| ORM | Django ORM |

---

## ⚙️ Инструкция по установке

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/your-username/taskflow.git
cd taskflow
```

### 2. Создайте и активируйте виртуальное окружение

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Установите зависимости

```bash
pip install django python-telegram-bot requests asgiref
```

### 4. Примените миграции базы данных

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Настройте токен Telegram-бота

Откройте `bot.py` и замените значение переменной `TOKEN` на токен вашего бота, полученный у [@BotFather](https://t.me/BotFather):

```python
TOKEN = "ВАШ_ТОКЕН_ЗДЕСЬ"
```

---

## 🚀 Инструкция по запуску

### Запуск веб-сервера Django

```bash
python manage.py runserver
```

Веб-интерфейс будет доступен по адресу: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### Запуск Telegram-бота

В отдельном терминале (при активированном виртуальном окружении):

```bash
python tasks/bot.py
```

В консоли появится сообщение `Bot is running...` — бот готов к работе.

> **Важно:** Django-сервер и бот работают независимо, но используют общую базу данных. Можно запускать оба одновременно.

---

## 💬 Примеры работы чат-бота

### `/start` — Приветствие
```
Пользователь: /start

Бот: Welcome to TodoChat-Bot!
     Use /help to see available commands.
```

### `/add` — Добавление задачи
```
Пользователь: /add

Бот: Enter task title:

Пользователь: Купить продукты

Бот: Task added: Купить продукты
```

### `/list` — Список задач
```
Пользователь: /list

Бот: Your tasks:
     1. Купить продукты ❌
        Priority: None  Deadline: None
     2. Сделать домашнее задание ✔
        Priority: High  Deadline: 2025-06-01 12:00:00
```

### `/complete` — Отметить задачу выполненной
```
Пользователь: /complete

Бот: Your tasks:
     1. Купить продукты ❌
        Priority: None  Deadline: None

     Enter task number to mark as completed:

Пользователь: 1

Бот: Marked as completed: Купить продукты
```

### `/priority` — Установка приоритета
```
Пользователь: /priority

Бот: Your tasks:
     1. Купить продукты ✔
        Priority: None  Deadline: None

     Enter task number to set priority:

Пользователь: 1

Бот: Current priority: None
     Enter new priority (Low, Medium, High):

Пользователь: High

Бот: Task priority updated: High
```

### `/deadline` — Установка дедлайна
```
Пользователь: /deadline

Бот: Enter task number to set deadline:

Пользователь: 1

Бот: Current deadline: None
     Enter new deadline (YYYY-MM-DD):

Пользователь: 2025-06-15

Бот: Task deadline updated: 2025-06-15
```

### `/search` — Поиск задачи
```
Пользователь: /search

Бот: Enter keyword:

Пользователь: продукты

Бот: Found tasks:
     1. Купить продукты ✔
        Priority: High  Deadline: None
```

### `/stats` — Статистика
```
Пользователь: /stats

Бот: Task Statistics:

     Total tasks: 5
     Completed tasks: 3
     Pending tasks: 2
```

### `/overdue` — Просроченные задачи
```
Пользователь: /overdue

Бот: Overdue tasks:

     1. Сдать отчёт ❌
        Priority: High  Deadline: 2025-05-01 00:00:00
```

### `/clear` — Очистить все задачи
```
Пользователь: /clear

Бот: All tasks cleared.
```

### Неизвестная команда
```
Пользователь: /random

Бот: Unknown command. Please use /help to see available commands.
     Не такая команды. Пожалуйста, используйте /help чтобы увидеть доступные команды.
```

---

## 🖥 Скриншоты интерфейса
### Главная страница — список задач и аналитика
<img width="1918" height="767" alt="Website" src="https://github.com/user-attachments/assets/db02fd04-0bf1-4373-9c95-0da648b3bea3" />
> Веб-интерфейс реализован в тёмной теме с боковой панелью аналитики слева и списком задач справа. Завершённые задачи отображаются перечёркнутым текстом. Приоритеты выделены цветом: 🔴 High, 🟡 Medium, 🟢 Low.

### Telegram-бот в действии
<img width="1246" height="965" alt="TelegramChatBot" src="https://github.com/user-attachments/assets/6a5700de-18a5-46cb-9bed-777f6021da57" />

### Django админка
<img width="1918" height="915" alt="Django Admin" src="https://github.com/user-attachments/assets/e16eafbe-dd34-424f-ace8-e2a0813ab734" />


## 📁 Структура проекта

```
To-doChatbot/
├── Screenshots/
│   ├── commands.png
│   ├── Django Admin.png
│   ├── TelegramChatBot.png
│   └── Website
├── taskflow/
│   ├── _pycache_/
│   ├── _init_.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tasks/
│   ├── _pycache_/
│   ├── migrations/
│   ├── _init_.py
│   ├── admin.py
│   ├── apps.py
│   ├── bot.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── templates/
│   └── index.html
├── db.sqlite
├── manage.py
├── README.md
└── requiriments.txt   
```

---

## 📋 Полный список команд бота

| Команда | Описание |
|---|---|
| `/start` | Запустить бота |
| `/help` | Показать все команды |
| `/add` | Добавить задачу |
| `/list` | Показать все задачи |
| `/delete` | Удалить задачу |
| `/complete` | Отметить задачу выполненной |
| `/edit` | Редактировать задачу |
| `/search` | Найти задачу по ключевому слову |
| `/priority` | Установить приоритет (Low / Medium / High) |
| `/deadline` | Установить дедлайн (YYYY-MM-DD) |
| `/overdue` | Показать просроченные задачи |
| `/stats` | Статистика задач |
| `/clear` | Удалить все задачи |
| `/cancel` | Отменить текущую операцию |
