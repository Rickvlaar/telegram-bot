from telegram import BotCommand, Bot
from telegram.ext import Updater, CommandHandler, Defaults, PrefixHandler
from telegram.utils.request import Request
from config import Config
import logging
import command_handlers
import conversation_handlers

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def ready_bot():
    defaults = Defaults(run_async=True)
    request = Request(con_pool_size=8)
    poep_bot = Bot(token=Config.AUTH_TOKEN, defaults=defaults, request=request)
    updater = Updater(bot=poep_bot, use_context=True)

    commands = []
    for command in command_handlers.no_param_handlers:
        this_chandler = CommandHandler(command=command.__name__, callback=command)
        this_prhandler = PrefixHandler('!', command=command.__name__, callback=command)
        updater.dispatcher.add_handler(this_prhandler)
        updater.dispatcher.add_handler(this_chandler)
        description = command_handlers.function_description_dict.get(command.__name__)
        commands.append(BotCommand(command=command.__name__, description=description))

    updater.dispatcher.add_handler(conversation_handlers.input_conversation_handler())
    poep_bot.set_my_commands(commands=commands)
    updater.start_polling()


ready_bot()
