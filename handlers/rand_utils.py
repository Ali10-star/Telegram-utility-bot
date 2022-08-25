from time import sleep
from telegram import Update
from telegram.ext import ContextTypes
from helpers.dice import icons
import random as rand

async def die(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('language', 'English')
    chat_id = update.message.chat_id
    result = rand.choice(list(range(1, 6)))
    text = 'لقد حصلت على:' if lang == 'Arabic' else 'You rolled a:'
    await context.bot.send_message(chat_id=chat_id, text=text)
    with open(icons[result], 'rb') as photo:
        await context.bot.send_photo(chat_id=chat_id, photo=photo)

async def rand_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('language', 'English')
    chat_id = update.message.chat_id
    start = int(context.args[0])
    end = int(context.args[1])
    result = rand.choice(list(range(start, end)))
    text = f'سأختار رقماً بين {start} و {end}' if lang == 'Arabic' else f"I'll choose a number between {start} and {end}"
    await context.bot.send_message(chat_id=chat_id, text=f'{text}:\n\n {result}')