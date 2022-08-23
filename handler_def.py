from handlers import wallpapers as wp
from handlers import reminder as rem
from handlers import rand_utils as rands
from handlers import inline
from handlers import data_store
from handlers import lang
from handlers import weather
from handlers import wolfram_handlers
from telegram.ext import CommandHandler, MessageHandler, filters, InlineQueryHandler, ConversationHandler
import handlers.generic_handlers as hnd

LANGUAGE = 0
REMINDER_DATE = 1
ALARM = 2

# start_handler = CommandHandler('start', hnd.start)
help_handler = CommandHandler('help', hnd.help_handler)

inline_search_handler = InlineQueryHandler(inline.inline_search_query)

# reminder_handler = CommandHandler('remind', rem.callback_timer)

die_handler = CommandHandler('die', rands.die)
rand_num_handler = CommandHandler('rand', rands.rand_number)

pexels_handler = CommandHandler('pexels', wp.pexels_handler)
unsplash_handler = CommandHandler('unsplash', wp.unsplash_handler)

store_handler = CommandHandler('mystore', data_store.show_user_data)
put_handler = CommandHandler('put', data_store.store_value)
get_handler = CommandHandler('get', data_store.show_value)
del_handler = CommandHandler('del', data_store.delete_value)
location_handler = CommandHandler("loc", data_store.location)
tzone_handler = CommandHandler("tzone", data_store.timezone)

start_handler = ConversationHandler(
        entry_points=[CommandHandler("start", hnd.start)],
        states={
            LANGUAGE: [MessageHandler(filters.Regex("^(English|Arabic)$"), hnd.language_config)],
        },
        fallbacks=[CommandHandler("cancel", hnd.cancel)],
    )

remind_handler = ConversationHandler(
    entry_points=[CommandHandler('remind', rem.reminder_handler)],
    states={
        REMINDER_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, rem.reminder_date_handler)],
    },
    fallbacks=[CommandHandler("cancel", hnd.cancel)],
    allow_reentry=True,
)

language_handler = CommandHandler("lang", lang.language_handler)
weather_handler = CommandHandler("weather", weather.weather_handler)

# WOLFRAM ALPHA
quick_handler = CommandHandler('quick', wolfram_handlers.quick_question)
equation_handler = CommandHandler('eq', wolfram_handlers.equation_solver)
boolean_handler = CommandHandler('bool', wolfram_handlers.boolean_algebra_solver)
plot_handler = CommandHandler('plot', wolfram_handlers.plotter)
plot3d_handler = CommandHandler('3dplot', wolfram_handlers.plotter3d)
wolfram_help_handler = CommandHandler('wolfram', wolfram_handlers.help)