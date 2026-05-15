import os
import sys
from turtle import title
import django

from asgiref.sync import sync_to_async

from telegram import Update

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters
)

# Django setup

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "taskflow.settings"
)

django.setup()

# Import Task model

from tasks import models
from tasks.models import Task

# Telegram Bot Token

TOKEN = "8694156051:AAFjGyMF-ECzfAdTD0hS7G0kl_H9IKMD_Ks"

# States for ConversationHandler

ADD_TASK, DELETE_TASK, SEARCH_TASK, COMPLETE_TASK = range(4)

# START

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Welcome to TodoChat-Bot!\n\n"
        "Commands:\n"
        "/add - Add task\n"
        "/list - Show tasks\n"
        "/delete - Delete task\n"
        "/complete - Complete task\n"
        "/search - Search task"
    )

# ADD TASK

async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Enter task title:"
    )

    return ADD_TASK

async def save_task(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = str(update.effective_user.id)

    user_name = update.effective_user.first_name or update.effective_user.username or "Unknown"

    title = update.message.text

    await sync_to_async(Task.objects.create)(
        user_id=user_id,
        user_name=user_name,
        title=title
    )

    await update.message.reply_text(
        f"Task added: {title}"
    )

    return ConversationHandler.END

# LIST TASKS

async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = str(update.effective_user.id)
    
    user_name = update.effective_user.first_name or update.effective_user.username or "Unknown"

    tasks = await sync_to_async(list)(
        Task.objects.filter(user_id=user_id)
    )

    if not tasks:

        await update.message.reply_text(
            "No tasks found."
        )

        return

    message = "Your tasks:\n\n"

    for i, task in enumerate(tasks, start=1):

        status = "✔" if task.completed else "❌"

        message += f"{i}. {task.title} {status}\n"

    await update.message.reply_text(message)

# DELETE TASK

async def delete_task(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = str(update.effective_user.id)
    
    user_name = update.effective_user.first_name or update.effective_user.username or "Unknown"

    tasks = await sync_to_async(list)(
        Task.objects.filter(user_id=user_id)
    )

    if not tasks:

        await update.message.reply_text(
            "No tasks to delete."
        )

        return ConversationHandler.END

    message = "Your tasks:\n\n"

    for i, task in enumerate(tasks, start=1):

        message += f"{i}. {task.title}\n"

    message += "\nEnter task number to delete:"

    await update.message.reply_text(message)

    return DELETE_TASK


async def remove_task(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = str(update.effective_user.id)

    tasks = await sync_to_async(list)(
        Task.objects.filter(user_id=user_id)
    )

    try:

        number = int(update.message.text)

        if 1 <= number <= len(tasks):

            deleted_task = tasks[number - 1]

            deleted_title = deleted_task.title

            await sync_to_async(deleted_task.delete)()

            await update.message.reply_text(
                f"Deleted task: {deleted_title}"
            )

        else:

            await update.message.reply_text(
                "Invalid task number."
            )

    except ValueError:

        await update.message.reply_text(
            "Please enter a valid number."
        )

    return ConversationHandler.END

# COMPLETE TASK

async def complete_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    tasks = await sync_to_async(list)(
        Task.objects.filter(user_id=user_id)
    )

    if not tasks:

        await update.message.reply_text(
            "No tasks to complete."
        )

        return ConversationHandler.END

    message = "Your tasks:\n\n"

    for i, task in enumerate(tasks, start=1):

        status = "✔" if task.completed else "❌"

        message += f"{i}. {task.title} {status}\n"

    message += "\nEnter task number to mark as completed:"

    await update.message.reply_text(message)

    return COMPLETE_TASK

async def mark_completed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    tasks = await sync_to_async(list)(
        Task.objects.filter(user_id=user_id)
    )

    try:

        number = int(update.message.text)

        if 1 <= number <= len(tasks):

            task = tasks[number - 1]

            task.completed = True

            await sync_to_async(task.save)()

            await update.message.reply_text(
                f"Marked as completed: {task.title}"
            )

        else:

            await update.message.reply_text(
                "Invalid task number."
            )

    except ValueError:

        await update.message.reply_text(
            "Please enter a valid number."
        )

    return ConversationHandler.END

# SEARCH TASK

async def search_task(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Enter keyword:"
    )

    return SEARCH_TASK


async def perform_search(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = str(update.effective_user.id)

    keyword = update.message.text

    tasks = await sync_to_async(list)(
        Task.objects.filter(
            user_id=user_id,
            title__icontains=keyword
        )
    )

    if tasks:

        message = "Found tasks:\n\n"

        for i, task in enumerate(tasks, start=1):
            status = "✔" if task.completed else "❌"
            message += f"{i}. {task.title} {status}\n"
    else:

        message = "No matching tasks found."

    await update.message.reply_text(message)

    return ConversationHandler.END

# CANCEL

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Operation cancelled."
    )

    return ConversationHandler.END

# UNKNOWN COMMAND

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Unknown command. Please use /start to see available commands."
    )

# =========================================================
# MAIN
# =========================================================

def main():

    app = ApplicationBuilder().token(TOKEN).build()

    # START
    app.add_handler(
        CommandHandler("start", start)
    )

    # LIST
    app.add_handler(
        CommandHandler("list", list_tasks)
    )

    # ADD
    add_handler = ConversationHandler(
        entry_points=[
            CommandHandler("add", add_task)
        ],

        states={
            ADD_TASK: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    save_task
                )
            ]
        },

        fallbacks=[
            CommandHandler("cancel", cancel)
        ]
    )

    # DELETE
    delete_handler = ConversationHandler(
        entry_points=[
            CommandHandler("delete", delete_task)
        ],

        states={
            DELETE_TASK: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    remove_task
                )
            ]
        },

        fallbacks=[
            CommandHandler("cancel", cancel)
        ]
    )
    
    # COMPLETE
    complete_handler = ConversationHandler(
        entry_points=[
            CommandHandler("complete", complete_task)
        ],

        states={
            COMPLETE_TASK: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    mark_completed
                )
            ]
        },

        fallbacks=[
            CommandHandler("cancel", cancel)
        ]
    )

    # SEARCH
    search_handler = ConversationHandler(
        entry_points=[
            CommandHandler("search", search_task)
        ],

        states={
            SEARCH_TASK: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    perform_search
                )
            ]
        },

        fallbacks=[
            CommandHandler("cancel", cancel)
        ]
    )
    

    app.add_handler(add_handler)
    app.add_handler(delete_handler)
    app.add_handler(complete_handler)
    app.add_handler(search_handler)
    app.add_handler(
        MessageHandler(
            filters.COMMAND,
            unknown
        )
    )

    print("Bot is running...")

    app.run_polling()

main()