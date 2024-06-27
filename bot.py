import logging
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes


TOKEN = ''
TARGET_CHAT_ID = ''

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def forward_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot = context.bot
    message = update.message

    logger.info(f"Received a message: {message}")

    if message.document:
        file_id = message.document.file_id
        await bot.send_document(chat_id=TARGET_CHAT_ID, document=file_id)
        logger.info(f"Forwarded a document: {file_id}")
    elif message.photo:
        file_id = message.photo[-1].file_id
        await bot.send_photo(chat_id=TARGET_CHAT_ID, photo=file_id)
        logger.info(f"Forwarded a photo: {file_id}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    forward_handler = MessageHandler(
        filters=filters.Document.ALL | filters.PHOTO | filters.VIDEO | filters.AUDIO | filters.VOICE | filters.Sticker.ALL,
        callback=forward_files
    )

    application.add_handler(forward_handler)

    application.run_polling()
