import os
import sys
from turtle import title
import django

from asgiref.sync import sync_to_async

from telegram import Update

from telegram.ext import (
    Application,
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

ADD_TASK, DELETE_TASK, SEARCH_TASK, COMPLETE_TASK, EDIT_TASK, SET_PRIORITY, DEADLINE_TASK, OVERDUE_TASK, STATS_TASK, CLEAR_TASK = range(10)

# START

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        """Welcome to TodoChat-Bot!
Use /help to see available commands."""
    )

# ADD TASK

async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Enter task title:"
    )

    return ADD_TASK
async def save_task(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = str(update.effective_user.id)

    title = update.message.text

    if title:

        await sync_to_async(Task.objects.create)(
            user_id=user_id,
            user_name=update.effective_user.full_name,
            title=title
        )

        await update.message.reply_text(
            f"Task added: {title}"
        )

    else:

        await update.message.reply_text(
            "Task title cannot be empty."
        )

    return ConversationHandler.END

# LIST TASKS

async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = str(update.effective_user.id)

    tasks = await sync_to_async(list)(
        Task.objects.filter(user_id=user_id)
    )

    if not tasks:

        await update.message.reply_text(
            "No tasks found."
        )

        return

    message = "Your tasks:\n"

    for i, task in enumerate(tasks, start=1):

        status = "✔" if task.completed else "❌"

        message += f"{i}. {task.title} {status}\n Priority: {task.priority} Deadline: {task.deadline}\n" 

    await update.message.reply_text(message)

# DELETE TASK

async def delete_task(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = str(update.effective_user.id)

    tasks = await sync_to_async(list)(
        Task.objects.filter(user_id=user_id)
    )

    if not tasks:

        await update.message.reply_text(
            "No tasks to delete."
        )

        return ConversationHandler.END

    message = "Your tasks:\n"

    for i, task in enumerate(tasks, start=1):
        status = "✔" if task.completed else "❌"

        message += f"{i}. {task.title} {status} \n Priority: {task.priority} Deadline: {task.deadline}\n"

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

    message = "Your tasks:\n"

    for i, task in enumerate(tasks, start=1):

        status = "✔" if task.completed else "❌"

        message += f"{i}. {task.title} {status}\n Priority: {task.priority} Deadline: {task.deadline}\n"

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

        message = "Found tasks:\n"

        for i, task in enumerate(tasks, start=1):
            status = "✔" if task.completed else "❌"
            message += f"{i}. {task.title} {status}\n Priority: {task.priority} Deadline: {task.deadline}\n"
    else:
        message = "No matching tasks found."

    await update.message.reply_text(message)

    return ConversationHandler.END

# EDIT TASK

async def edit_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    tasks = await sync_to_async(list)(
        Task.objects.filter(user_id=user_id)
    )

    if not tasks:

        await update.message.reply_text(
            "No tasks to edit."
        )

        return ConversationHandler.END

    message = "Your tasks:\n"

    for i, task in enumerate(tasks, start=1):

        status = "✔" if task.completed else "❌"

        message += f"{i}. {task.title} {status}\n Priority: {task.priority} Deadline: {task.deadline}\n"

    message += "\nEnter task number to edit:"

    await update.message.reply_text(message)

    return EDIT_TASK

async def save_edited_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    tasks = await sync_to_async(list)(
        Task.objects.filter(user_id=user_id)
    )

    try:

        number = int(update.message.text)

        if 1 <= number <= len(tasks):

            task = tasks[number - 1]

            await update.message.reply_text(
                f"Current title: {task.title}\nEnter new title:"
            )

            context.user_data['edit_task_id'] = task.id

            return EDIT_TASK

        else:

            await update.message.reply_text(
                "Invalid task number."
            )

    except ValueError:

        new_title = update.message.text

        task_id = context.user_data.get('edit_task_id')

        if task_id:

            task = await sync_to_async(Task.objects.get)(id=task_id)

            task.title = new_title

            await sync_to_async(task.save)()

            await update.message.reply_text(
                f"Task updated: {new_title}"
            )

        else:

            await update.message.reply_text(
                "No task selected for editing."
            )

    return ConversationHandler.END

# PRIORITY TASK
async def set_priority(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    tasks = await sync_to_async(list)(
        Task.objects.filter(user_id=user_id)
    )

    if not tasks:

        await update.message.reply_text(
            "No tasks to set priority."
        )

        return ConversationHandler.END

    message = "Your tasks:\n"

    for i, task in enumerate(tasks, start=1):

        status = "✔" if task.completed else "❌"

        message += f"{i}. {task.title} {status}\n Priority: {task.priority} Deadline: {task.deadline}\n"

    message += "\nEnter task number to set priority:"

    await update.message.reply_text(message)

    return SET_PRIORITY

async def save_priority(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    tasks = await sync_to_async(list)(
        Task.objects.filter(user_id=user_id)
    )

    try:
        number = int(update.message.text)

        if 1 <= number <= len(tasks):

            task = tasks[number - 1]

            await update.message.reply_text(
                f"Current priority: {task.priority}\nEnter new priority (Low, Medium, High):"
            )

            context.user_data['priority_task_id'] = task.id

            return SET_PRIORITY

        else:

            await update.message.reply_text(
                "Invalid task number."
            )

    except ValueError:
        new_priority = update.message.text

        task_id = context.user_data.get('priority_task_id')

        if task_id:

            task = await sync_to_async(Task.objects.get)(id=task_id)

            task.priority = new_priority

            await sync_to_async(task.save)()

            await update.message.reply_text(
                f"Task priority updated: {new_priority}"
            )

        else:

            await update.message.reply_text(
                "No task selected for setting priority."
            )

    return ConversationHandler.END

# DEADLINE TASK
async def deadline_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    tasks = await sync_to_async(list)(
        Task.objects.filter(user_id=user_id)
    )

    if not tasks:

        await update.message.reply_text(
            "No tasks to set deadline."
        )

        return ConversationHandler.END

    message = "Your tasks:\n"

    for i, task in enumerate(tasks, start=1):

        status = "✔" if task.completed else "❌"

        message += f"{i}. {task.title} {status}\n Priority: {task.priority} Deadline: {task.deadline}\n"

    message += "\nEnter task number to set deadline:"

    await update.message.reply_text(message)

    return DEADLINE_TASK

async def save_deadline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    tasks = await sync_to_async(list)(
        Task.objects.filter(user_id=user_id)
    )

    new_deadline = update.message.text.split()[-1] if update.message.text.split()[-1].lower().startswith("deadline:") else None

    try:
        number = int(update.message.text)

        if 1 <= number <= len(tasks):

            task = tasks[number - 1]

            await update.message.reply_text(
                f"Current deadline: {task.deadline}\nEnter new deadline (YYYY-MM-DD):"
            )

            context.user_data['deadline_task_id'] = task.id

            return DEADLINE_TASK

        else:

            await update.message.reply_text(
                "Invalid task number."
            )

    except ValueError:
        new_deadline = update.message.text

        task_id = context.user_data.get('deadline_task_id')

        if task_id:

            task = await sync_to_async(Task.objects.get)(id=task_id)

            task.deadline = new_deadline

            await sync_to_async(task.save)()

            await update.message.reply_text(
                f"Task deadline updated: {new_deadline}"
            )

        else:

            await update.message.reply_text(
                "No task selected for setting deadline."
            )

    return ConversationHandler.END

# OVERDUE TASKS

async def overdue_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    tasks = await sync_to_async(list)(
        Task.objects.filter(user_id=user_id, deadline__lt=django.utils.timezone.now(), completed=False)
    )

    if not tasks:

        await update.message.reply_text(
            "No overdue tasks found."
        )

        return

    message = "Overdue tasks:\n\n"

    for i, task in enumerate(tasks, start=1):
        status = "✔" if task.completed else "❌"
        message += f"{i}. {task.title} {status}\n Priority: {task.priority} Deadline: {task.deadline}\n\n"

    await update.message.reply_text(message)
    
# STATS
async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    total_tasks = await sync_to_async(Task.objects.filter(user_id=user_id).count)()

    completed_tasks = await sync_to_async(Task.objects.filter(user_id=user_id, completed=True).count)()

    pending_tasks = total_tasks - completed_tasks

    message = (
        f"Task Statistics:\n\n"
        f"Total tasks: {total_tasks}\n"
        f"Completed tasks: {completed_tasks}\n"
        f"Pending tasks: {pending_tasks}"
    )

    await update.message.reply_text(message)
    
# CLEAR TASKS
async def clear_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    await sync_to_async(Task.objects.filter(user_id=user_id).delete)()

    await update.message.reply_text(
        "All tasks cleared."
    )

# HELP

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Commands:\n"
        "/add - Add task\n"
        "/list - Show tasks\n"
        "/delete - Delete task\n"
        "/complete - Complete task\n"
        "/search - Search task\n"
        "/edit - Edit task\n"
        "/priority - Set task priority\n"
        "/deadline - Set task deadline\n"
        "/overdue - Show overdue tasks\n"
        "/stats - Show task statistics\n"
        "/clear - Clear all tasks\n"
        "/help - Show commands\n"
    )

# CANCEL

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Operation cancelled."
    )

    return ConversationHandler.END

# UNKNOWN COMMAND

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Unknown command. Please use /help to see available commands.\n"
        "Не такая команды. Пожалуйста, используйте /help чтобы увидеть доступные команды."
    )
    
# Unknown MESSAGE

async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "What you're writing, you can only write commands. Use /help to see available commands.\n"
        "Че пишешь, ты можешь писать только команды. Используй /help чтобы увидеть доступные команды."
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
    
    # LIST
    app.add_handler(
        CommandHandler("list", list_tasks)
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
    
    # EDIT
    edit_handler = ConversationHandler(
        entry_points=[
            CommandHandler("edit", edit_task)
        ],

        states={
            EDIT_TASK: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    save_edited_task
                )
            ]
        },

        fallbacks=[
            CommandHandler("cancel", cancel)
        ]
    )
    
    # PRIORITY
    priority_handler = ConversationHandler(
        entry_points=[
            CommandHandler("priority", set_priority)
        ],

        states={
            SET_PRIORITY: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    save_priority
                )
            ]
        },

        fallbacks=[
            CommandHandler("cancel", cancel)
        ]
    )
    
    # DEADLINE
    deadline_handler = ConversationHandler(
        entry_points=[
            CommandHandler("deadline", deadline_task)
        ],

        states={
            DEADLINE_TASK: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    save_deadline
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
    app.add_handler(edit_handler)
    app.add_handler(priority_handler)
    app.add_handler(deadline_handler)
    app.add_handler(CommandHandler("overdue", overdue_tasks))
    app.add_handler(CommandHandler("stats", show_stats))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("clear", clear_tasks))
    app.add_handler(CommandHandler("cancel", cancel))
    app.add_handler(MessageHandler(filters.COMMAND,unknown_command))
    app.add_handler(MessageHandler(filters.TEXT, unknown_message))

    print("Bot is running...")

    app.run_polling()
main()