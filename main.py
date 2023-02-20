import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import dotenv_values

config = dotenv_values('.env')

TOKEN = config['TOKEN']

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger("INFOLOGGER")

async def start(update, context):
    await update.message.reply_text(("The bot's been started"))

async def echo(update, context):
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

def main():
    if __name__ == '__main__':
        logger.info("The bot's been started")
        application = Application.builder().token(TOKEN).build()

        application.add_handler(CommandHandler('start', start))
        application.add_handler(MessageHandler(filters.TEXT, echo))

        application.run_polling()

if __name__ == '__main__':
    main()