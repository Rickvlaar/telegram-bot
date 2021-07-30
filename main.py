from telegram import BotCommand, Bot
from telegram.ext import Updater, CommandHandler, PrefixHandler
from config import Config
from scheduled_jobs import get_expired_bets
import asyncio
import logging
import command_handlers
import conversation_handlers

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def ready_poepbot() -> Bot:
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
    return poep_bot


def ready_hhpc_bot() -> Bot:
    hhpc_bot = Bot(token=Config.HHPC_TOKEN, defaults=Config.DEFAULTS, request=Config.REQUEST)
    updater = Updater(bot=hhpc_bot, use_context=True)

    insultees = [member.strip() for member in Config.MEMBERS.split(',')]
    for name in insultees:
        logging.log(logging.ERROR, name)
        updater.dispatcher.add_handler(CommandHandler(command=name, callback=command_handlers.send_insult))

    updater.dispatcher.add_handler(CommandHandler(command='insult', callback=command_handlers.insult))
    updater.dispatcher.add_handler(CommandHandler(command='adjekratje', callback=command_handlers.adje_kratje))
    updater.dispatcher.add_handler(CommandHandler(command='kratjes', callback=command_handlers.kratjes))

    commands = list()
    commands.append(BotCommand(command='voornaam', description='Beledig iemand, bv: /Adolf '))
    commands.append(BotCommand(command='insult', description='Voeg een nieuwe belediging toe aan de database'))
    commands.append(BotCommand(command='kratjes', description='Overzicht van alle onzinnige weddenschappen'))
    commands.append(BotCommand(command='adjekratje', description='Voeg weddenschap toe, -s --stake "inzet", -b --better "de wedder", -d --date "tot wanneer in yyyy-mm-dd"\n'
                        'voorbeeld: /adjekratje rutte liegt 100 keer -b henk -s 1 kratje -d 2020-01-01'))

    updater.dispatcher.add_handler(conversation_handlers.input_conversation_handler())
    hhpc_bot.set_my_commands(commands=commands)

    updater.start_polling()
    return hhpc_bot


def ready_bots():
    poepbot = ready_poepbot()
    hhpc_bot = ready_hhpc_bot()
    asyncio.run(get_expired_bets(hhpc_bot))


ready_bots()
