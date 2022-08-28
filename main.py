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

if __name__ == '__main__':
    API_KEY = os.getenv('API_KEY')
    ENV = os.getenv('ENV', 'DEV')
    bot_config = BotConfig(API_KEY)
    bot_config.register_handlers(handlers_list)

    if ENV == 'DEV':
        bot_config.run()
    else:
        updater = Updater(bot=Bot(API_KEY), update_queue=Queue())
        WEB_HOOK = f"https://utility-telegram-bot.onrender.com"
        run( updater.start_webhook(listen="0.0.0.0", port=5000, url_path=API_KEY, webhook_url=f"{WEB_HOOK}/{API_KEY}") )

