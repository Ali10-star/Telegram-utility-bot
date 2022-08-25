import requests as req
from telegram import Update
import random as rand
from telegram.ext import ContextTypes
from dotenv import load_dotenv
import os

load_dotenv()

# Globals
FETCHING_WALL = ""
NOT_FOUND = ""
TAKEN_BY = ""
ON = ""
LINK = ""
ERROR = ""

async def pexels_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    is_search = len(context.args) != 0
    is_arabic = context.user_data.get('language', 'English') == 'Arabic'
    set_text_constants(is_arabic)
    chat_id = update.message.chat_id
    bot = context.bot
    await bot.send_message(chat_id=chat_id, text=f'{FETCHING_WALL}[Pexels](https://www.pexels.com)', parse_mode='MarkdownV2')
    if is_search:
        search_query = ' '.join(context.args[0:])
        photo_link, preview, photographer, photographer_url, status = search_pexels(search_query)
        if not photo_link:
            await bot.send_message(chat_id=chat_id, text=f'{NOT_FOUND} "{search_query}".')
            return
    else:
        photo_link, preview, photographer, photographer_url, status = fetch_random_pexels()

    if status == 200:
        await bot.send_photo(chat_id=update.effective_chat.id, photo=preview,
                                     caption=f"{TAKEN_BY} [{photographer}]({photographer_url})",
                                     parse_mode='MarkdownV2')
        await bot.send_message(chat_id=chat_id, text=f'[{LINK}]({photo_link})', disable_web_page_preview=True, parse_mode='MarkdownV2')
    else:
        await bot.send_message(chat_id=chat_id, text=f'{ERROR} {status}')


async def unsplash_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    is_search = len(context.args) != 0
    chat_id = update.message.chat_id
    is_arabic = context.user_data.get('language', 'English') == 'Arabic'
    set_text_constants(is_arabic)
    bot = context.bot
    await bot.send_message(chat_id=chat_id, text=f'{FETCHING_WALL}Unsplash...')
    if is_search:
        search_query = ' '.join(context.args[0:])
        photo_link, preview, taken_by, username, status = search_unsplash(search_query)
        if not photo_link:
            await bot.send_message(chat_id=chat_id, text=f'{NOT_FOUND} "{search_query}".')
            return
    else:
        photo_link, preview, taken_by, username, status = fetch_random_unsplash()

    if status == 200:
        await bot.send_photo(chat_id=update.effective_chat.id, photo=preview,
                                     caption=f"{TAKEN_BY} [{taken_by}](https://unsplash.com/@{username}){ON}[Unsplash](https://www.unsplash.com/)",
                                     parse_mode='MarkdownV2')
        await bot.send_message(chat_id=chat_id, text=f'[{LINK}]({photo_link})', disable_web_page_preview=True, parse_mode='MarkdownV2')
    else:
        await bot.send_message(chat_id=chat_id, text=f'{ERROR} {status}')

async def nasa_apod(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    is_arabic = context.user_data.get('language', 'English') == 'Arabic'
    API_KEY = os.getenv('NASA_API_KEY')
    URL = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}"
    response = req.get(URL).json()
    date = response['date']
    explanation = response['explanation']
    title = response['title']
    url = response['url']
    hd_url = response['hdurl']
    await context.bot.send_photo(chat_id=chat_id, photo=url, caption=f"Title: {title}, Taken on: {date}")
    await context.bot.send_message(chat_id=chat_id, text=f'<b>Explanation:</b> {explanation}', disable_web_page_preview=True, parse_mode='html')
    MSG = 'رابط الصورة بدقة أعلى' if is_arabic else "Link to the photo in higher resolution"
    await context.bot.send_message(chat_id=chat_id, text=f'[{MSG}]({hd_url})', disable_web_page_preview=True, parse_mode='MarkdownV2')

async def nasa_images(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    is_arabic = context.user_data.get('language', 'English') == 'Arabic'
    query = " ".join(context.args[0:]) if context.args else "Apollo"
    URL = f"https://images-api.nasa.gov/search?q={query}&media_type=image"
    response = req.get(URL).json()
    collection = response['collection']
    items = collection['items']
    total_items_count = len(items)
    if not total_items_count:
        ERROR = 'لم أعثر على نتائج تطابق بحثك.' if is_arabic else 'No images match your search query.'
        await context.bot.send_message(chat_id=chat_id, text=ERROR, disable_web_page_preview=True)
        return
    index = rand.choice(list(range(0, total_items_count)))
    data = items[index]
    center = data['data'][0]['center']
    date_created = data['data'][0]['date_created']
    description = data['data'][0]['description']
    thumbnail = data['links'][0]['href']
    actual_image = (req.get(data['href'])).json()[0]
    await context.bot.send_photo(chat_id=chat_id, photo=thumbnail, caption=f"<b>Description:</b> {description}\n<b>Created on:</b> {date_created}", parse_mode='html')
    await context.bot.send_message(chat_id=chat_id, text=f'<b>Center: </b> {center}', disable_web_page_preview=True, parse_mode='html')
    MSG = 'رابط الصورة بدقة أعلى' if is_arabic else "Link to the photo in higher resolution"
    await context.bot.send_message(chat_id=chat_id, text=f'[{MSG}]({actual_image})', disable_web_page_preview=True, parse_mode='MarkdownV2')


def search_pexels(search_query: str):
    URL = 'https://api.pexels.com/v1/search?query='
    API_KEY = os.getenv('PEXELS_API_KEY')
    headers = {'Authorization': API_KEY}
    response = req.get(URL + search_query, headers=headers)
    found_photos = response.json()['photos']
    if response.status_code != 200 or not found_photos:
        return [], [], [], [], response.status_code
    selected_photo = rand.choice( response.json()['photos'] )
    photo_link = selected_photo['src']['original']
    preview = selected_photo['src']['medium']
    photographer = selected_photo['photographer']
    photographer_url = selected_photo['photographer_url']
    return photo_link, preview, photographer, photographer_url, response.status_code

def fetch_random_pexels():
    URL = 'https://api.pexels.com/v1/curated'
    API_KEY = os.getenv('PEXELS_API_KEY')
    headers = {'Authorization': API_KEY}
    response = req.get(URL, headers=headers)
    json_res = response.json()
    selected_photo = rand.choice( json_res['photos'] )
    photo_link = selected_photo['src']['original']
    preview = selected_photo['src']['medium']
    photographer = selected_photo['photographer']
    photographer_url = selected_photo['photographer_url']
    return photo_link, preview, photographer, photographer_url, response.status_code


def fetch_random_unsplash():
    ACCESS_KEY = os.getenv('UNSPLASH_API_KEY')
    URL = f"https://api.unsplash.com/photos/random/?client_id={ACCESS_KEY}"
    response = req.get(URL)
    json_res = response.json()
    status_code = response.status_code
    photo_url = json_res["urls"]["full"]
    taken_by = json_res['user']['name']
    taken_by_username = json_res['user']['username']
    preview = json_res["urls"]["small"]
    return photo_url, preview, taken_by, taken_by_username, status_code

def search_unsplash(search_query: str):
    ACCESS_KEY = os.getenv('UNSPLASH_API_KEY')
    URL = f"https://api.unsplash.com/search/photos?query={search_query}&client_id={ACCESS_KEY}"
    response = req.get(URL)
    json_res = response.json()
    status_code = response.status_code
    num_results_found = len(json_res["results"])
    if not num_results_found:
        return [], [], [], [], status_code
    photo_id = rand.choice( list(range(0,  num_results_found)) )
    photo_url = json_res["results"][photo_id]["urls"]["full"]
    taken_by = json_res["results"][photo_id]['user']['name']
    taken_by_username = json_res["results"][photo_id]['user']['username']
    preview = json_res["results"][photo_id]["urls"]["small"]
    return photo_url, preview, taken_by, taken_by_username, status_code


def set_text_constants(is_arabic: bool) -> None:
    global FETCHING_WALL, NOT_FOUND, TAKEN_BY, ON, LINK, ERROR
    FETCHING_WALL = ' جارٍ جلب الصورة من' if is_arabic else 'Fetching wallpaper from '
    NOT_FOUND = 'لم يتم العثور على صورة تطابق البحث: ' if is_arabic else 'No photos found for: '
    TAKEN_BY = 'تم التقاط الصورة من قبل ' if is_arabic else 'Taken by '
    ON = ' على ' if is_arabic else ' on '
    LINK = ' رابط الصورة بالدقة الكاملة ' if is_arabic else ' Link to full resolution photo '
    ERROR = 'حدث خطأ ما، رمز الخطأ: ' if is_arabic else 'Something went wrong. Status code: '