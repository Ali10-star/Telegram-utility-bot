from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from html import escape
from uuid import uuid4

async def inline_search_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the inline query. This is run when you type: @botusername <query>"""
    query = update.inline_query.query
    if query == "":
        return

    TRANSLATE_TO_ARABIC_URL = f"https://translate.google.com/?sl=en&tl=ar&text={escape(query)}&op=translate"
    WIKIPEDIA_URL = f"https://en.wikipedia.org/wiki/{escape(query)}"
    YOUTUBE_URL = f"https://www.youtube.com/results?search_query={escape(query)}"
    BING_URL = f"https://www.bing.com/search?q={escape(query)}"
    GOOGLE_URL = f"https://www.google.com/search?q={escape(query)}"
    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Wikipedia",
            input_message_content=InputTextMessageContent(WIKIPEDIA_URL, parse_mode=ParseMode.HTML
            ),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="YouTube",
            input_message_content=InputTextMessageContent(YOUTUBE_URL, parse_mode=ParseMode.HTML
            ),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Google Translate (AR)",
            input_message_content=InputTextMessageContent(TRANSLATE_TO_ARABIC_URL, parse_mode=ParseMode.HTML
            ),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Bing",
            input_message_content=InputTextMessageContent(BING_URL, parse_mode=ParseMode.HTML
            ),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Google",
            input_message_content=InputTextMessageContent(GOOGLE_URL, parse_mode=ParseMode.HTML
            ),
        ),
    ]
    await update.inline_query.answer(results)
