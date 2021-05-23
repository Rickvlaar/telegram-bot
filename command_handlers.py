import telegram.ext
import logging
from util import process_input
from data_model import ItemList, Item, db_session


def krishan(update: telegram.Update, context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Krishan is een luie drol')


def rolf(update: telegram.Update, context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Rolf baft tarrelige anussen')


def steven(update: telegram.Update, context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Steven pijpt drollen')


def rick(update: telegram.Update, context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Bedenkt zelf lekker iets')


def new(update: telegram.Update, context: telegram.ext.CallbackContext):
    list_name, args = process_input(update.message.text)
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
    items = [str(index + 1) + '. ' + item.item_name + ' (' + item.created_by + ')\n'for index, item in enumerate(item_list)]
    pleepapier_string = pleepapier_string + ''.join(items)
    context.bot.send_message(chat_id=update.effective_chat.id, text=pleepapier_string)
    session.close()


def reservelijst(update: telegram.Update, context: telegram.ext.CallbackContext):
    list_name = 'Reservelijst'
    session = db_session()
    item_list = session.query(Item).filter(Item.item_list == list_name).order_by(Item.id).all()
    reservelijst_string = 'Reservelijst:\n'
    items = [str(index + 1) + '. ' + item.item_name + ' (' + item.created_by + ')\n' for index, item in enumerate(item_list)]
    reservelijst_string = reservelijst_string + ''.join(items)
    context.bot.send_message(chat_id=update.effective_chat.id, text=reservelijst_string)
    session.close()


def add(update: telegram.Update, context: telegram.ext.CallbackContext):
    list_name = 'Pleepapier'
    added_message = ''
    try:
        item_to_add, args = process_input(update.message.text)
        if args:
            if '--reserve' in args or '-r' in args:
                list_name = 'Reservelijst'
        session = db_session()
        item = Item(item_name=item_to_add, item_list=list_name, created_by=update.effective_user.first_name)
        session.add(item)
        session.commit()
        session.close()
        added_message += '"' + item_to_add + '"' + ' staat erop!'
    except ValueError:
        added_message = 'retard...'
        pass
    context.bot.send_message(chat_id=update.effective_chat.id, text=added_message)


def remove(update: telegram.Update, context: telegram.ext.CallbackContext):
    list_name = 'Pleepapier'
    removed_message = ''
    try:
        command, args = process_input(update.message.text)
        if args:
            if '--reserve' in args or '-r' in args:
                list_name = 'Reservelijst'
        session = db_session()
        if command.isdigit():
            remove_index = int(command) - 1
            item = session.query(Item).filter(Item.item_list == list_name).order_by(Item.id).all()[remove_index]
        else:
            item = session.query(Item).filter(Item.item_list == list_name, Item.item_name == command).first()
        if not item:
            raise ValueError
        session.delete(item)
        session.commit()
        session.close()
        removed_message += '"' + item.item_name + '" is eraf!'
    except (AttributeError, TypeError) as e:
        logging.exception(e)
        removed_message += 'Ben je dom ofzo?'
        pass
    except IndexError:
        removed_message += 'Dit nummer staat niet op de lijst mongol'
        pass
    except ValueError:
        removed_message += 'Dit item staat niet op de lijst mongol'
        pass
    context.bot.send_message(chat_id=update.effective_chat.id, text=removed_message)


function_description_dict = {
        'krishan': 'Scheld Krishan uit',
        'rolf': 'Scheld Rolf uit',
        'steven': 'Scheld Steven uit',
        'rick': 'Scheld Rick uit',
        'pleepapier': 'Print het pleepapier uit',
        'reservelijst': 'Print de reservelijst uit',
        'add': 'Voeg item toe aan pleepapier, -r --reserve voegt toe aan reservelijst',
        'remove': 'Verwijder item van pleepapier, -r --reserve verwijdert van reservelijst',
        'new': 'Maak een nieuw papiertje aan'
}
