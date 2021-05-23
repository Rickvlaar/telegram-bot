from telegram import BotCommand, Bot
from telegram.ext import Updater, CommandHandler, Defaults, PrefixHandler
from telegram.utils.request import Request
from config import Config, ready_env
from inspect import getmembers, isfunction
import util
import logging
import command_handlers


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def ready_bot():
    ready_env()
    if not util.check_data_model():
        util.drop_all_tables(True)
        util.create_data_model()

    defaults = Defaults(run_async=True)
    request = Request(con_pool_size=8)
    poep_bot = Bot(token=Config.AUTH_TOKEN, defaults=defaults, request=request)
    updater = Updater(bot=poep_bot, use_context=True)

    commands = []
    for command, func in getmembers(command_handlers, isfunction):
        if command in command_handlers.function_description_dict.keys():
            updater.dispatcher.add_handler(CommandHandler(command=command, callback=func))
            updater.dispatcher.add_handler(PrefixHandler('!', command=command, callback=func))
            description = command_handlers.function_description_dict.get(command)
            commands.append(BotCommand(command=command, description=description))

    poep_bot.set_my_commands(commands=commands)
    updater.start_polling()


ready_bot()
