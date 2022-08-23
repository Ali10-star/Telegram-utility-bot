import wolframalpha as wa
import os
import requests
import urllib.parse
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes
from helpers.help import WOLFRAM_HELP, WOLFRAM_HELP_ARABIC

load_dotenv()

APP_ID = os.getenv('WOLFRAM_APP_ID')
URL = "http://api.wolframalpha.com/v2/query?"
client = wa.Client(APP_ID)
WOLFRAM_LINK = f"https://www.wolframalpha.com/input?i="

async def equation_solver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id, args, is_arabic = setup(update, context)
    bot = context.bot
    if not args:
        await context.bot.send_message(chat_id=chat_id, text="You must enter an equation for me to solve.")
        return

    equation = " ".join(args[0:])
    query = urllib.parse.quote_plus(f"solve {equation}")
    query_url = f"{URL}appid={APP_ID}" \
                f"&input={query}" \
                f"&scanner=Solve" \
                f"&podstate=Result__Step-by-step+solution" \
                "&format=plaintext" \
                f"&output=json"

    r = requests.get(query_url).json()
    data = r["queryresult"]["pods"][0]["subpods"]
    result = data[0]["plaintext"]
    steps = data[1]["plaintext"]
    await bot.send_message(chat_id=chat_id, text=f"{result}")
    await bot.send_message(chat_id=chat_id, text=f"{steps}")

    MSG = "الحل الكامل على WolframAlpha" if is_arabic else "Full solution on WolframAlpha"
    await bot.send_message(chat_id=chat_id, text=f'[{MSG}]\n({WOLFRAM_LINK + equation})', disable_web_page_preview=True)

async def quick_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id, args, _ = setup(update, context)
    if not args:
        await context.bot.send_message(chat_id=chat_id, text=f"Invalid query, please try again.")
        return

    question = " ".join(context.args[0:])
    try:
        res = client.query(question)
        answer = next(res.results).text
        await context.bot.send_message(chat_id=chat_id, text="Getting answer from WolframAlpha...")
        await context.bot.send_message(chat_id=chat_id, text=answer)
    except:
        await context.bot.send_message(chat_id=chat_id, text="No answer found.")

async def boolean_algebra_solver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id, args, is_arabic = setup(update, context)
    bot = context.bot

    if not args:
        await context.bot.send_message(chat_id=chat_id, text="You must enter a boolean expression for me to solve.")
        return

    formula = " ".join(args[0:])
    # formula = "((P AND (Q IMPLIES R)) OR S) AND T"
    query = urllib.parse.quote_plus(f"solve {formula}")
    query_url = f"http://api.wolframalpha.com/v2/query?" \
                f"appid={APP_ID}" \
                f"&input={query}" \
                f"&output=json" \
                f"&includepodid=Input" \
                f"&includepodid=MinimalForms" \
                f"&includepodid=TruthDensity"

    r = requests.get(query_url).json()

    pods = r["queryresult"]["pods"]
    expression = pods[0]["subpods"][0]["plaintext"]
    min_forms = "\n".join(pods[1]["subpods"][0]["plaintext"].split("\n")[:-1])
    truth_density = pods[2]["subpods"][0]["plaintext"].split("=")

    await bot.send_message(chat_id=chat_id, text=f"Expression:  {expression}")
    await bot.send_message(chat_id=chat_id, text=f"{min_forms}")
    await bot.send_message(chat_id=chat_id, text=f"Truth density equals {truth_density[0]} which is {truth_density[1]}")


async def plotter3d(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id, args, is_arabic = setup(update, context)
    if not args:
        await context.bot.send_message(chat_id=chat_id, text="You must enter a boolean expression for me to solve.")
        return

    function = " ".join(args[0:])
    query = f"plot {function}"
    query_url = f"http://api.wolframalpha.com/v2/query?" \
                f"appid={APP_ID}" \
                f"&input={query}" \
                f"&output=json" \
                f"&includepodid=3DPlot" \
                f"&includepodid=ContourPlot"

    r = requests.get(query_url).json()

    pods = r["queryresult"]["pods"]
    plot_3d_url = pods[0]["subpods"][0]["img"]["src"]
    plot_contour_url = pods[1]["subpods"][0]["img"]["src"]
    await context.bot.send_message(chat_id=chat_id, text="Plotting...")
    await context.bot.send_photo(chat_id=chat_id, photo=plot_3d_url, caption=f"3D plot of {function}")
    await context.bot.send_photo(chat_id=chat_id, photo=plot_contour_url, caption=f"Contour of {function}")

    MSG = "الرسم بكامل التفاصيل على WolframAlpha" if is_arabic else "Full plot details on WolframAlpha"
    await context.bot.send_message(chat_id=chat_id, text=f'[{MSG}]\n{WOLFRAM_LINK}plot+{function}', disable_web_page_preview=True)

async def plotter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id, args, is_arabic = setup(update, context)
    if not args:
        await context.bot.send_message(chat_id=chat_id, text="You must enter a boolean expression for me to solve.")
        return

    function = " ".join(args[0:])
    query = f"plot {function}"
    query_url = f"http://api.wolframalpha.com/v2/query?" \
                f"appid={APP_ID}" \
                f"&input={query}" \
                f"&output=json"
    r = requests.get(query_url).json()
    plot = r["queryresult"]["pods"][1]["subpods"][0]["img"]["src"]
    await context.bot.send_message(chat_id=chat_id, text="Plotting...")
    await context.bot.send_photo(chat_id=chat_id, photo=plot, caption=f"Plot of {function}")

    MSG = "الرسم بكامل التفاصيل على WolframAlpha" if is_arabic else "Full plot details on WolframAlpha"
    await context.bot.send_message(chat_id=chat_id, text=f'[{MSG}]\n{WOLFRAM_LINK}plot+{function}', disable_web_page_preview=True)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_lang = context.user_data.get('language', 'English')
    msg = WOLFRAM_HELP_ARABIC if user_lang == 'Arabic' else WOLFRAM_HELP
    await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, disable_web_page_preview=True)



def setup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    args = context.args
    is_arabic = True if context.user_data.get('language', 'English') == 'Arabic' else False

    return chat_id, args, is_arabic