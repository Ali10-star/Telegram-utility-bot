from config import BotConfig
from dotenv import load_dotenv
import handler_def as handlers
import logging_config
import os

load_dotenv()
logging_config.setup_logging()

if __name__ == '__main__':
    API_KEY = os.getenv('API_KEY')
    bot_config = BotConfig(API_KEY)
    application = bot_config.get_application()
    job_queue = application.job_queue

    bot_config.register_handlers(
    [
        handlers.start_handler,
        handlers.help_handler,
        # reminder
        handlers.remind_handler,
        # random utils
        handlers.die_handler,
        handlers.rand_num_handler,
        # wallpapers
        handlers.pexels_handler,
        handlers.unsplash_handler,
        handlers.inline_search_handler,
        # Data Store
        handlers.store_handler,
        handlers.put_handler,
        handlers.get_handler,
        handlers.del_handler,
        handlers.language_handler,
        handlers.weather_handler,
    ])

    bot_config.run()
