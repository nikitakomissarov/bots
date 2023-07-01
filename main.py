import json
import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import dotenv_values
from google.cloud import dialogflow
import logging
from logging.handlers import TimedRotatingFileHandler

config = dotenv_values('.env')

TG_CHAT_ID = config['TG_CHAT_ID']
TG_TOKEN = config['TG_TOKEN']
GOOGLE_APPLICATION_CREDENTIALS = config['GOOGLE_APPLICATION_CREDENTIALS']
TRAINING_PHRASES = config['TRAINING_PHRASES']

with open(TRAINING_PHRASES, "r") as phrases_file:
  training_phrases_parts = phrases_file.read()
  training_phrases_parts = json.loads(training_phrases_parts)

with open(GOOGLE_APPLICATION_CREDENTIALS, "r") as my_file:
    credentials = my_file.read()
    credentials = json.loads(credentials)

logger = logging.getLogger('Logger')
logger_info = logging.getLogger('loggerinfo')
logger_error = logging.getLogger("loggererror")

handler = TimedRotatingFileHandler("app.log", when='D', interval=30, backupCount=1)
handler_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class TelegramLogsHandler(logging.Handler):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    def emit(self, record):
        log_entry = self.format(record)
        asyncio.create_task(self.send_log_message(log_entry))

    async def send_log_message(self, log_entry):
        await self.bot.send_message(chat_id=TG_CHAT_ID, text=log_entry)


def detect_intent_texts(project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    logger_info.info("Session path: {}\n".format(session))

    text_input = dialogflow.TextInput(text=texts, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    logger_info.info("=" * 20)
    logger_info.info("Query text: {}".format(response.query_result.query_text))
    logger_info.info(
        "Detected intent: {} (confidence: {})\n".format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence,
        ))

    if response.query_result.intent.is_fallback is True \
            or response.query_result.intent_detection_confidence == 0:
        logger_error.error('Нулевое совпадение')
        return None
    else:
        answer = (format(response.query_result.fulfillment_text))
        return answer

async def start(update, context):
    await update.message.reply_text("The bot's been started")

async def echo(update, context: ContextTypes.DEFAULT_TYPE):
    try:
        language_code = update.message.from_user.language_code
        text = update.message.text
        session_id = update.message.chat['id']
        google_reply = detect_intent_texts(credentials['quota_project_id'], session_id, text, language_code)
        if google_reply != None:
            google_reply = google_reply
        else:
            google_reply = 'Я вас не понимаю'
        await context.bot.send_message(chat_id=update.effective_chat.id, text=google_reply)

    except Exception as err:
        logger_error.error(err, exc_info=True)

def main():
    if __name__ == '__main__':
        application = Application.builder().token(TG_TOKEN).build()
        bot = application.bot

        handler.setFormatter(handler_format)

        logger_info.setLevel(logging.INFO)
        logger_info.addHandler(handler)

        logger_error.setLevel(logging.ERROR)
        logger_error.addHandler(handler)

        telegram_notification_handler = TelegramLogsHandler(bot)
        telegram_notification_handler.setFormatter(handler_format)
        logger_error.addHandler(telegram_notification_handler)

        logger_info.info("here we go")

        try:
            application.add_handler(CommandHandler('start', start))
            application.add_handler(MessageHandler(filters.TEXT, echo))
            application.run_polling()

        except Exception as err:
            logger_error.error(err, exc_info=True)

if __name__ == '__main__':
    main()