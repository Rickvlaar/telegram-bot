from telegram import BotCommand, Bot
from telegram.ext import Updater, CommandHandler, PrefixHandler
from config import Config
import logging
import command_handlers
import conversation_handlers

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def ready_poepbot():
    poep_bot = Bot(token=Config.AUTH_TOKEN, defaults=Config.DEFAULTS, request=Config.REQUEST)
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


def ready_hhpc_bot():
    hhpc_bot = Bot(token=Config.HHPC_TOKEN, defaults=Config.DEFAULTS, request=Config.REQUEST)
    updater = Updater(bot=hhpc_bot, use_context=True)

    insultees = [member.strip() for member in Config.MEMBERS.split(',')]
    for name in insultees:
        updater.dispatcher.add_handler(CommandHandler(command=name, callback=command_handlers.send_insult))
        updater.dispatcher.add_handler(PrefixHandler('!', command=name, callback=command_handlers.send_insult))

    hhpc_bot.commands.append(BotCommand(command='{{voornaam}}', description='Beledig iemand; !{{voornaam}} werkt ook; ex: "/Adolf", "!Adolf"'))
    updater.start_polling()


def ready_bots():
    ready_poepbot()
    ready_hhpc_bot()


ready_bots()
