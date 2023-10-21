import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Инструкция")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректный запрос!")


async def create_deadline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="create_deadline")


async def get_deadlines(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="get_deadlines")


if __name__ == '__main__':
    application = ApplicationBuilder().token('5394641313:AAEdGWxVKNLGKn_iXeTsttAH5BB2IL-mMxM').build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    create_deadline_handler = CommandHandler('create_deadline', create_deadline)
    application.add_handler(create_deadline_handler)

    get_deadlines_handler = CommandHandler('get_deadlines', get_deadlines)
    application.add_handler(get_deadlines_handler)

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

    application.run_polling()
