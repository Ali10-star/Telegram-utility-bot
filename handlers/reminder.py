import dateparser
import datetime
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, ContextTypes

# Globals
REMINDER_DATE = 1
TEXT = ""
IS_ARABIC = False

async def reminder_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global TEXT, IS_ARABIC
    IS_ARABIC = context.user_data.get('language', 'English') == 'Arabic'
    args = context.args
    TEXT = " ".join( args[0:] ) if args else " "
    MSG = ".حسناً أرسل لي الوقت الذي تريد ضبط المذكرة عليه" if IS_ARABIC else "OK, send me the time to set for the reminder."
    EXAMPLE = "مثال: خلال 30 دقيقة (أو) 30 دقيقة" if IS_ARABIC else "E.g. in 30 minutes (or) 30 minutes"
    await update.message.reply_text(MSG + "\n" + EXAMPLE)
    return REMINDER_DATE

async def send_reminder(context: CallbackContext):
    MSG = "<b>مذكرة:</b>" if IS_ARABIC else "<b>Reminder:</b>"
    await context.bot.send_message(chat_id=context.job.chat_id, text=f'{MSG} {context.job.data}', parse_mode="html")

async def reminder_date_handler(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    reminder_time = fix_input_date(update.message.text)

    duration = dateparser.parse(reminder_time, languages=['en', 'ar'])
    if duration is None or duration < datetime.datetime.utcnow():
        ERROR = "التاريخ غير صحيح، الرجاء المحاولة مرة أخرى." if IS_ARABIC else "Invalid date, please try again."
        await context.bot.send_message(chat_id=chat_id, text=f'{ERROR}')

    REMINDER_SET = "تم ضبط المذكرة!" if IS_ARABIC else "Reminder set!"
    await update.message.reply_text(f'{REMINDER_SET}')

    context.job_queue.run_once(send_reminder, get_seconds(duration), data=TEXT, chat_id=chat_id)
    return ConversationHandler.END

def fix_input_date(in_time: str) -> str:
    result = in_time
    if IS_ARABIC:
        if 'خلال' not in in_time:
            result = 'خلال ' + in_time
    else:
        if 'in' not in in_time:
            result = 'in ' + in_time
    return result

def get_seconds(duration: datetime) -> int:
    now = datetime.datetime.now()
    time = duration - now
    return time.total_seconds()