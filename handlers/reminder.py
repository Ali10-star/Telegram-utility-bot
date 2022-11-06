import dateparser
import datetime
import re
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, ContextTypes

# Globals
REMINDER_DATE = 1
TEXT = ""
IS_ARABIC = False

def current_timestamp() -> float:
    return datetime.datetime.timestamp(datetime.datetime.now())

async def reminder_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global TEXT, IS_ARABIC, TIMEZONE
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
    user_message = update.message.text
    err_flag = False

    if user_message.startswith("*"):
        duration = parse_time_string(user_message)
    else:
        reminder_time = fix_input_date(in_time=user_message)
        duration = get_seconds(dateparser.parse(reminder_time, languages=['en', 'ar']))

        if float(duration) < 0:
           err_flag = True

    if duration is None or err_flag:
        ERROR = "التاريخ غير صحيح، الرجاء المحاولة مرة أخرى." if IS_ARABIC else "Invalid date, please try again."
        await context.bot.send_message(chat_id=chat_id, text=f'{ERROR}')

    REMINDER_SET = "تم ضبط المذكرة!" if IS_ARABIC else "Reminder set!"
    await update.message.reply_text(f'{REMINDER_SET}')

    context.job_queue.run_once(send_reminder, duration, data=TEXT, chat_id=chat_id)
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
    now = datetime.datetime.now(tz=None)
    time = duration - now
    return time.total_seconds()

def parse_time_string(time_string: str) -> int:
    # Example: '1w 1d 2h 3m 4s'
    weeks = re.findall(r'\d+w', time_string)
    weeks = 0 if len(weeks) == 0 else int(weeks[0][:-1])

    days = re.findall(r'\d+d', time_string)
    days = 0 if len(days) == 0 else int(days[0][:-1])

    hours = re.findall(r'\d+h', time_string)
    hours = 0 if len(hours) == 0 else int(hours[0][:-1])

    minutes = re.findall(r'\d+m', time_string)
    minutes = 0 if len(minutes) == 0 else int(minutes[0][:-1])

    seconds = re.findall(r'\d+s', time_string)
    seconds = 0 if len(seconds) == 0 else int(seconds[0][:-1])
    time = datetime.timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds)
    return time.total_seconds()