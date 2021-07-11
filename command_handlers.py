import telegram.ext
import logging
from telegram import ForceReply
from util import process_input, get_random_insult, get_insultee_name
from command_helpers import add_item, move_item, remove_item, add_insult, get_kratjes, set_next_episode, add_bet
from conversation_handlers import ConversationStates
from data_model import ItemList, Item, db_session


def send_insult(update: telegram.Update, context: telegram.ext.CallbackContext):
    name = get_insultee_name(update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=get_random_insult(name))


def krishan(update: telegram.Update, context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=get_random_insult('Krishan'))


def rolf(update: telegram.Update, context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=get_random_insult('Rolf'))


def steven(update: telegram.Update, context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=get_random_insult('Steven'))


def rick(update: telegram.Update, context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=get_random_insult('Rick'))


def luuk(update: telegram.Update, context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=get_random_insult('Luuk'))


def new(update: telegram.Update, context: telegram.ext.CallbackContext):
    command = process_input(update.message.text)
    list_name = command.value
    response = ''
    try:
        session = db_session()
        existing_list = session.query(ItemList).filter(ItemList.list_name == list_name).all()
        if len(existing_list) > 0:
            response += 'Gast "' + list_name + '" bestaat al...'
        else:
            item_list = ItemList(list_name=list_name, created_by=update.effective_user.first_name)
            session.add(item_list)
            session.commit()
            response += '"' + list_name + '" is aangemaakt!'
        session.close()
    except ValueError:
        response += 'Lullo, je moet wel wat invullen he'
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)


def pleepapier(update: telegram.Update, context: telegram.ext.CallbackContext):
    list_name = 'Pleepapier'
    session = db_session()
    item_list = session.query(Item).filter(Item.item_list == list_name).order_by(Item.id).all()
    pleepapier_string = 'Pleepapier:\n'
    items = [str(index + 1) + '. ' + item.item_name + ' (' + item.created_by + ')\n' for index, item in
             enumerate(item_list)]
    pleepapier_string = pleepapier_string + ''.join(items)
    context.bot.send_message(chat_id=update.effective_chat.id, text=pleepapier_string)
    session.close()


def reservelijst(update: telegram.Update, context: telegram.ext.CallbackContext):
    list_name = 'Reservelijst'
    session = db_session()
    item_list = session.query(Item).filter(Item.item_list == list_name).order_by(Item.id).all()
    reservelijst_string = 'Reservelijst:\n'
    items = [str(index + 1) + '. ' + item.item_name + ' (' + item.created_by + ')\n' for index, item in
             enumerate(item_list)]
    reservelijst_string = reservelijst_string + ''.join(items)
    context.bot.send_message(chat_id=update.effective_chat.id, text=reservelijst_string)
    session.close()


def add(update: telegram.Update, context: telegram.ext.CallbackContext):
    try:
        add_item(update, context)
    except ValueError:
        return request_missing_input(update, context, ConversationStates.ADD_INPUT_MISSING)


def rm(update: telegram.Update, context: telegram.ext.CallbackContext):
    try:
        remove_item(update, context)
    except (AttributeError, TypeError) as e:
        logging.exception(e)
        context.bot.send_message(chat_id=update.effective_chat.id, text='Ben je dom ofzo?')
        pass
    except (ValueError, IndexError):
        return request_missing_input(update, context, ConversationStates.RM_INPUT_MISSING)


def move(update: telegram.Update, context: telegram.ext.CallbackContext):
    try:
        move_item(update, context)
    except (AttributeError, TypeError) as e:
        logging.exception(e)
        context.bot.send_message(chat_id=update.effective_chat.id, text='Ben je dom ofzo?')
        pass
    except (ValueError, IndexError):
        return request_missing_input(update, context, ConversationStates.MOVE_INPUT_MISSING)


def insult(update: telegram.Update, context: telegram.ext.CallbackContext):
    try:
        add_insult(update, context)
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Wel wat invullen he....')
        # return request_missing_input(update, context, ConversationSt/ates.INSULT_INPUT_MISSING)


def kratjes(update: telegram.Update, context: telegram.ext.CallbackContext):
    try:
        get_kratjes(update, context)
    except ValueError as e:
        logging.exception(e)
        pass


def adje_kratje(update: telegram.Update, context: telegram.ext.CallbackContext):
    try:
        add_bet(update, context)
    except ValueError as e:
        logging.exception(e)
        error_message = 'Voeg weddenschap toe, -s --stake "inzet", -b --better "de wedder", -d --date "tot wanneer in yyyy-mm-dd"\n ' \
                        'voorbeeld: /adjekratje rutte liegt 100 keer -b henk -s 1 kratje -d 2020-01-01'
        context.bot.send_message(chat_id=update.effective_chat.id, text=error_message)
        pass


def volgende(update: telegram.Update, context: telegram.ext.CallbackContext):
    try:
        set_next_episode(update=update, context=context)
    except ValueError as e:
        logging.exception(e)
        pass


def request_missing_input(update: telegram.Update, context: telegram.ext.CallbackContext, conversation_state: int):
    no_input_message = 'Wat dan lullo?'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             reply_to_message_id=update.message.message_id,
                             text=no_input_message,
                             reply_markup=ForceReply(selective=True))
    return conversation_state


function_description_dict = {
        'krishan':      'Scheld Krishan uit',
        'rolf':         'Scheld Rolf uit',
        'steven':       'Scheld Steven uit',
        'rick':         'Scheld Rick uit',
        'luuk':         'Scheld Luuk uit',
        'pleepapier':   'Print het pleepapier uit',
        'reservelijst': 'Print de reservelijst uit',
        'add':          'Voeg item toe aan pleepapier, -r --reserve voegt toe aan reservelijst',
        'rm':           'Verwijder item van pleepapier, -r --reserve verwijdert van reservelijst',
        'move':         'Verplaats item naar reservelijst, -r --reserve haalt item van reservelijst',
        'new':          'Maak een nieuw papiertje aan',
        'insult':       'Voeg een nieuwe belediging toe aan de database',
        'adjekratje':   'Voeg weddenschap toe, -s --stake "inzet", -b --better "de wedder", -d --date "tot wanneer in yyyy-mm-dd"\n' \
                        'voorbeeld: /adjekratje rutte liegt 100 keer -b henk -s 1 kratje -d 2020-01-01'
}

no_param_handlers = [
        krishan,
        rolf,
        steven,
        rick,
        luuk,
        pleepapier,
        reservelijst
]

input_handlers = [
        add,
        rm,
        move,
        new,
        insult,
        volgende
]
