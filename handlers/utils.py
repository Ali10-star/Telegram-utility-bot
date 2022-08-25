import requests as req
from telegram import Update
from telegram.ext import ContextTypes

async def ip_getter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_lang = context.user_data.get('language', 'English')
    URL = "https://api.ipify.org/?format=json"
    response = req.get(URL).json()
    MSG = 'عنوان الIP الخاص بك هو :' if user_lang == 'Arabic' else "Your IP address is: "
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{MSG}{response['ip']}", disable_web_page_preview=True)
1