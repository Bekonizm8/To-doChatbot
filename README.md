# To-Do Chatbot

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

# Installation Instruction
## 1. Install Python

Download and install Python from:
https://www.python.org/

## 2. Install Required Libraries

Open terminal inside the project folder and run:

pip install -r requirements.txt

# Launch Insruction

## 1. Apply Database Migrations

Run:

python manage.py makemigrations
python manage.py migrate

## 2. Create Admin User

Run:

python manage.py createsuperuser

Enter:
- username
- email
- password

## 3. Start Django Server

Run:

python manage.py runserver

Open browser:

http://127.0.0.1:8000/

Admin panel:

http://127.0.0.1:8000/admin/

## 4. Configure Telegram Bot

Open:
tasks/bot.py

Find:

TOKEN = "8694156051:AAFjGyMF-ECzfAdTD0hS7G0kl_H9IKMD_Ks"

Replace with your Telegram Bot token.

## 5. Start Telegram Bot

Open second terminal and run:

python tasks/bot.py

# Screenshots

## Telegram Chatbot
<img width="1246" height="965" alt="TelegramChatBot" src="https://github.com/user-attachments/assets/af3b79a3-3fd8-410a-b119-b6411783a88e" />

## Django Admin
<img width="1918" height="915" alt="Django Admin" src="https://github.com/user-attachments/assets/c4e3cf01-967e-47ce-b8cf-c22cb3dae70d" />
