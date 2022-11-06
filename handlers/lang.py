from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler
from helpers.help import HELP_MESSAGE
from logging_config import logger

supported_strings = ("Arabic", "arabic", "العربية", "عربي", "English", "english")
async def language_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.message.chat_id
    selected_lang = context.args[0] if context.args else "English"
    if selected_lang not in supported_strings:
        await context.bot.send_message(chat_id=chat_id, text=f'Sorry, I don\'t understand "{selected_lang}"\nEnglish will be used instead.')
        context.user_data['language'] = "English"
        return

    text = "OK! I will remember to use English from now on."
    if selected_lang in ["Arabic", "arabic", "العربية", "عربي"]:
        selected_lang = "Arabic"
        text = ".حسناً سأتذكر أن أستخدم العربية من الآن فصاعداً"

    await context.bot.send_message(chat_id=chat_id, text=text)
    context.user_data['language'] = selected_lang