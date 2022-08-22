import os
from datetime import datetime
import requests as http_client
from telegram import Update
from telegram.ext import ContextTypes
from dotenv import load_dotenv
from helpers.weather_help import get_weather_report

load_dotenv()
API_KEY = os.getenv('OPEN_WEATHER_API_KEY')
URL = 'http://api.openweathermap.org/data/2.5/weather'

async def weather_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    bot = context.bot
    is_arabic = context.user_data.get('language', 'English') == 'Arabic'
    query = " ".join(context.args[0:] ) if context.args else context.user_data.get('location', "London")
    MSG = get_message(is_arabic, query)
    params = {'q': query, 'appid': API_KEY, 'units': 'metric', 'lang': 'ar' if is_arabic else 'en'}
    response = http_client.get(URL, params=params)
    if response.status_code == 404:
        NOT_FOUND = "لم يتم العثور على الموقع" if is_arabic else "Location not found"
        await bot.send_message(chat_id=chat_id, text=NOT_FOUND, parse_mode='MarkdownV2')
        return
    json = response.json()
    icon_id = json['weather'][0]['icon']
    icon_url = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"

    report = get_weather_report(json, is_arabic)
    await bot.send_message(chat_id=chat_id, text=MSG, parse_mode='MarkdownV2')
    await bot.send_photo(chat_id=chat_id, photo=icon_url, caption=report)


def get_message(is_arabic: bool, query: str) -> str:
    return f"ها هي النشرة الجوية اليوم في {query}" if is_arabic else f"Here's Today's weather forecast in {query}"