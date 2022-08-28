from config import BotConfig
from dotenv import load_dotenv
from handler_def import handlers_list
from telegram import Bot
from telegram.ext import Updater
from asyncio import run, Queue
import logging_config
import os

load_dotenv()
logging_config.setup_logging()
WEB_HOOK = f"https://utility-telegram-bot.onrender.com"
API_KEY = os.getenv('API_KEY')
PORT = int(5000)
ENV = os.getenv('ENV', 'DEV')

if __name__ == '__main__':
    bot_config = BotConfig(API_KEY)
    bot_config.register_handlers(handlers_list)
    application = bot_config.get_application()
    # run(application.bot.set_webhook(url=f"{WEB_HOOK}/{API_KEY}"))
    if ENV == 'DEV':
        bot_config.run()
    else:
        run(application.run_webhook(listen="0.0.0.0", port=PORT, url_path=API_KEY,
                                    webhook_url=f"{WEB_HOOK}/{API_KEY}"))

