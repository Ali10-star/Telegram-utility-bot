from urllib import response
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler
from helpers.help import HELP_MESSAGE, HELP_MESSAGE_ARABIC
from logging_config import logger
import requests as req

# Globals
LANGUAGE = 0

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [["English", "Arabic"]]
    name = get_user_name(update)
    await update.message.reply_text(
        f"Hi {name}!\nI'm a utility bot. \n"
        "What language would you like to use?\n\n\n"
        f"مرحباً يا{name} ، أنا بوت مساعد"
        "\n"
        "ما اللغة التي تريد استخدامها؟",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="English or Arabic?"
        ),
    )
    return LANGUAGE

async def language_config(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = update.message.text if update.message.text in ["English", "Arabic"] else "English"
    context.user_data['language'] = lang
    text = "OK! I will remember to use English from now on."
    if context.user_data['language'] == 'Arabic':
        text = ".حسناً سأتذكر أن أستخدم العربية من الآن فصاعداً"

    await update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "OK, I will use English as the default language.", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_lang = context.user_data.get('language', 'English')
    msg = HELP_MESSAGE_ARABIC if user_lang == 'Arabic' else HELP_MESSAGE
    await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, disable_web_page_preview=True)

def get_user_name(update: Update) -> str:
    name = update.message.from_user.first_name
    return "" if name is None else " " + name