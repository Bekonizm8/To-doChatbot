# To-DoChatbot Manager

## Project Description

To-doChatbot is a hybrid To-Do management system created using Django and Telegram Bot API.

The project allows users to:

- Add tasks
- Delete tasks
- Search tasks
- View task list
- Mark tasks as completed

The system works through:

- Telegram Bot
- Django Web Interface
- SQLite Database

---

# Technologies Used

- Python
- Django
- SQLite
- python-telegram-bot
- HTML/CSS

---

# Features

## Telegram Bot

Commands:

- /start
- /add
- /list
- /delete
- /search

## Django Web Interface

- Add tasks
- Delete tasks
- Complete tasks
- Admin panel
- Task list

---

# Project Structure

TaskFlow/
│
├── manage.py
├── db.sqlite3
│
├── taskflow/
│
├── tasks/
│   ├── models.py
│   ├── views.py
│   ├── bot.py
│   ├── admin.py
│
├── templates/
│   └── index.html
│
├── requirements.txt
│
└── README.md

---

# Installation

## 1. Clone project

```bash
git clone https://github.com/yourusername/taskflow.git