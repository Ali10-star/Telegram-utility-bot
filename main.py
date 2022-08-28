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
PORT = 5000
ENV = os.getenv('ENV', 'DEV')

# async def start_webhook():
#     updater = Updater(bot=Bot(API_KEY), update_queue=Queue()):
#     async with updater:
#         await updater.start_webhook(listen="0.0.0.0", port=5000, url_path=API_KEY, webhook_url=f"{WEB_HOOK}/{API_KEY}")

if __name__ == '__main__':
    bot_config = BotConfig(API_KEY)
    bot_config.register_handlers(handlers_list)
    application = bot_config.get_application()
    # run(application.bot.set_webhook(url=f"{WEB_HOOK}/{API_KEY}"))
    if ENV == 'DEV':
        print("In development (:")
        bot_config.run()
    else:
        print("In production!")
        run(application.run_webhook(listen="127.0.0.1", port=PORT, url_path=API_KEY,
                                    webhook_url=f"{WEB_HOOK}/{API_KEY}"))

