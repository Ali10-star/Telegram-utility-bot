from telegram.ext import Application, ApplicationBuilder

class BotConfig:
    def __init__(self, token: str) -> None:
        self.__application = ApplicationBuilder().token(token).build()

    def get_application(self) -> Application:
        return self.__application

    def register_handlers(self, handlers: list) -> None:
        for handler in handlers:
            self.__application.add_handler(handler)

    def run(self) -> None:
        self.__application.run_polling()