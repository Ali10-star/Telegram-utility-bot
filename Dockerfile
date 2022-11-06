FROM python:3.10

WORKDIR /Telegram-utility-bot

RUN pip3 install -r requirements.txt

CMD python3 main.py
