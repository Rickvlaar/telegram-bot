from telegram import BotCommand, Bot
from telegram.ext import Updater, CommandHandler, Defaults
from telegram.utils.request import Request
from config import Config
from inspect import getmembers, isfunction
import command_handlers


import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def ready_bot():
    defaults = Defaults(run_async=True)
    request = Request(con_pool_size=8)
    poep_bot = Bot(token=Config.AUTH_TOKEN, defaults=defaults, request=request)
    updater = Updater(bot=poep_bot, use_context=True)

    commands = []
    for command, func in getmembers(command_handlers, isfunction):
        updater.dispatcher.add_handler(CommandHandler(command=command, callback=func))
        commands.append(BotCommand(command=command, description='test'))

    poep_bot.set_my_commands(commands=commands)
    updater.start_polling()


ready_bot()
