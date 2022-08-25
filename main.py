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
        handlers.myip_handler,
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
        handlers.location_handler,
        handlers.tzone_handler,
        # Wolfram Alpha
        handlers.quick_handler,
        handlers.equation_handler,
        handlers.boolean_handler,
        handlers.plot_handler,
        handlers.plot3d_handler,
        handlers.wolfram_help_handler,
        handlers.apod_handler,
        handlers.nasa_search_handler,
    ])

    bot_config.run()
