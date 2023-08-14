import json
import logging
from logging.handlers import TimedRotatingFileHandler
from dotenv import dotenv_values
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from intent_detection import detect_intent_texts
from logger import TelegramLogsHandler, bot_logger


config = dotenv_values('.env')
TG_TOKEN = config['TG_TOKEN']
GOOGLE_APPLICATION_CREDENTIALS = config['GOOGLE_APPLICATION_CREDENTIALS']

logger_info = logging.getLogger('loggerinfo')
logger_error = logging.getLogger("loggererror")


class Communication:

    def __init__(self, project_id):
        self.project_id = project_id

    async def start(self, update, context: ContextTypes.DEFAULT_TYPE):
        try:
            await update.message.reply_text("The bot's been started")
        except Exception:
            logger_error.exception('Error')

    async def reply(self, update, context: ContextTypes.DEFAULT_TYPE):
        try:
            language_code = update.message.from_user.language_code
            text = update.message.text
            session_id = update.message.chat['id']
            google_reply = detect_intent_texts(
                self.project_id, session_id, text, language_code
            )
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=google_reply.fulfillment_text)


def main():
    handler = TimedRotatingFileHandler("app.log", when='D', interval=30, backupCount=1)
    handler_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(handler_format)
    logger_info.setLevel(logging.INFO)
    logger_info.addHandler(handler)
    logger_error.setLevel(logging.ERROR)
    logger_error.addHandler(handler)
    telegram_notification_handler = TelegramLogsHandler(bot_logger)
    telegram_notification_handler.setFormatter(handler_format)
    logger_error.addHandler(telegram_notification_handler)

    try:
        with open(GOOGLE_APPLICATION_CREDENTIALS, "r") as google_file:
            credentials = google_file.read()
            credentials = json.loads(credentials)
            _, _, id_tuple, _, _ = credentials.items()
            _, project_id = id_tuple

        application = Application.builder().token(TG_TOKEN).build()

        filled_handlers = Communication(project_id)
        application.add_handler(CommandHandler('start', filled_handlers.start))
        application.add_handler(MessageHandler(filters.TEXT, filled_handlers.reply))
        application.run_polling()

        logger_info.info("here we go")

    except Exception:
        logger_error.exception('Error')


if __name__ == '__main__':
    main()
