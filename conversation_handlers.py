from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters, CallbackContext, PrefixHandler
from command_helpers import add_item, remove_item, move_item
import command_handlers


class ConversationStates:
    ADD_INPUT_MISSING = 0
    RM_INPUT_MISSING = 1
    MOVE_INPUT_MISSING = 2


def no_add_input(update: Update, context: CallbackContext) -> int:
    try:
        add_item(update, context)
        return ConversationHandler.END
    except ValueError:
        return ConversationStates.ADD_INPUT_MISSING


def no_rm_input(update: Update, context: CallbackContext) -> int:
    try:
        remove_item(update, context)
        return ConversationHandler.END
    except ValueError:
        return ConversationStates.RM_INPUT_MISSING


def no_move_input(update: Update, context: CallbackContext) -> int:
    try:
        move_item(update, context)
        return ConversationHandler.END
    except ValueError:
        return ConversationStates.MOVE_INPUT_MISSING


def input_conversation_handler() -> ConversationHandler:
    handlers = [CommandHandler(command=func.__name__, callback=func) for func in command_handlers.input_handlers]
    handlers += [PrefixHandler('!', command=func.__name__, callback=func) for func in command_handlers.input_handlers]

    input_conversation = ConversationHandler(
            entry_points=handlers,
            states={
                    ConversationStates.ADD_INPUT_MISSING : [
                            MessageHandler(filters=Filters.text, callback=no_add_input)],
                    ConversationStates.RM_INPUT_MISSING  : [MessageHandler(filters=Filters.text, callback=no_rm_input)],
                    ConversationStates.MOVE_INPUT_MISSING: [
                            MessageHandler(filters=Filters.text, callback=no_move_input)],
            },
            fallbacks=[CommandHandler('rick', command_handlers.rick)],
    )
    return input_conversation
