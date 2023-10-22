import db
from config import TOKEN
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Инструкция")


async def create_deadline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    all_message = update.message.text.split()
    date = all_message[1]
    task = all_message[2]
    db.insert_into_db(
        user_name=update.effective_user.username,
        date_str=date,
        task=task
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Дедлайн сохранен")


async def get_deadlines(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = db.get_from_db(user_name=update.effective_user.username)
    message = []
    for elem in tasks:
        message.append(f"{elem['deadline']} {elem['task']}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text='\n'.join(message))


async def delete_deadline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    task = update.message.text.split()[1]
    db.remove_from_db(user_name=update.effective_user.username, task=task)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Дедлайн удален")


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('create_deadline', create_deadline))
    application.add_handler(CommandHandler('get_deadlines', get_deadlines))
    application.add_handler(CommandHandler('delete_deadline', delete_deadline))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

    application.run_polling()
