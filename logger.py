import logging
import asyncio
from dotenv import dotenv_values
from telegram.ext import Application


config = dotenv_values('.env')
TG_CHAT_ID = config['TG_CHAT_ID']
TG_LOGGER_TOKEN = config['TG_LOGGER_TOKEN']

application_logger = Application.builder().token(TG_LOGGER_TOKEN).build()
bot_logger = application_logger.bot


class TelegramLogsHandler(logging.Handler):

    def __init__(self, bot_logger):
        super().__init__()
        self.bot_logger = bot_logger

    def emit(self, record):
        log_entry = self.format(record)
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.create_task(self.bot_logger.send_message(chat_id=TG_CHAT_ID, text=log_entry))
        else:
            loop.run_until_complete(self.bot_logger.send_message(chat_id=TG_CHAT_ID, text=log_entry))
