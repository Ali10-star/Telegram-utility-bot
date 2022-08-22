from telegram import Update
from telegram.ext import ContextTypes

async def show_user_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('language', 'English')
    MESSAGE = "هذا كل شيء قمت بتخزينه" if lang == "Arabic" else "This is everything you had me store"
    chat_id = update.message.chat_id
    bot = context.bot
    context.user_data['name'] = update.message.from_user.first_name
    await bot.send_message(chat_id=chat_id,
                           text=f"{MESSAGE}:\n\n{dict_to_str(context.user_data)}",
                           parse_mode='html')

async def store_value(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('language', 'English')
    chat_id = update.message.chat_id
    bot = context.bot
    user_data = context.user_data
    key = str(context.args[0])
    value = " ".join( context.args[1:])
    if key not in user_data:
        context.user_data[key] = value
    else:
        MSG = "هذا المفتاح موجود مسبقا" if lang == "Arabic" else "This key is already exists."
        await bot.send_message(chat_id=chat_id, text=f"{MSG}")

    CONFIRM = "تم إضافة القيمة بنجاح" if lang == "Arabic" else "Value added successfully."
    await bot.send_message(chat_id=chat_id, text=f"{CONFIRM}")

async def show_value(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('language', 'English')
    chat_id = update.message.chat_id
    bot = context.bot
    key = str(context.args[0])
    if key in context.user_data:
        value = context.user_data[key]
        await bot.send_message(chat_id=chat_id, text=f"<b>{key}</b>: {value}", parse_mode='html')
    else:
        MSG = "لم أعثر على قيمة تطابق هذا المفتاح" if lang == "Arabic" else "I couldn't find a value matching this key."
        await bot.send_message(chat_id=chat_id, text=f"{MSG}")

async def delete_value(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('language', 'English')
    chat_id = update.message.chat_id
    bot = context.bot
    key = str(context.args[0])
    removed_value = context.user_data.pop(key, None)
    if not removed_value:
        MSG = "آسف، هذا المفتاح غير موجود، لا يمكنني حذفه." if lang == "Arabic" else "Sorry, this key is not found, I can't delete it."
        await bot.send_message(chat_id=chat_id, text=f"{MSG}")

    MSG = "تم حذف القيمة بنجاح" if lang == "Arabic" else "Value deleted successfully."
    await bot.send_message(chat_id=chat_id, text=f"{MSG}")

def dict_to_str(dictionary: dict) -> str:
    return "\n".join(f"<b>{key}</b>: {value}" for key, value in dictionary.items())
