from telegram.ext import Application, Updater
from telegram import Bot
from asyncio import Queue

class BotConfig:
    def __init__(self, token: str) -> None:
        # .token("TOKEN")
        self.application = Application.builder() \
                            .updater(Updater(bot=Bot(token), update_queue=Queue)) \
                            .build()

    def get_application(self) -> Application:
        return self.application

    def register_handlers(self, handlers: list) -> None:
        for handler in handlers:
            self.application.add_handler(handler)

    def run(self) -> None:
        self.application.run_polling()