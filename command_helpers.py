import telegram.ext
from util import upsert_record, process_input, delete_record
from data_model import Item, db_session


def add_item(update: telegram.Update, context: telegram.ext.CallbackContext):
    command, args = process_input(update.message.text)
    list_name = 'Pleepapier'
    if args:
        if '--reserve' in args or '-r' in args:
            list_name = 'Reservelijst'
    item = Item(item_name=command, item_list=list_name, created_by=update.effective_user.first_name)
    upsert_record(item)
    input_received_message = '"' + command + '"' + ' staat erop!'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=input_received_message)


def remove_item(update: telegram.Update, context: telegram.ext.CallbackContext):
    command, args = process_input(update.message.text)
    item = query_item(command, args)
    if not item:
        raise ValueError
    delete_record(item)
    removed_message = '"' + item.item_name + '" is eraf!'
    context.bot.send_message(chat_id=update.effective_chat.id, text=removed_message)


def move_item(update: telegram.Update, context: telegram.ext.CallbackContext):
    command, args = process_input(update.message.text)
    item = query_item(command, args)
    if not item:
        raise ValueError
    item.item_list = 'Pleepapier' if item.item_list == 'Reservelijst' else 'Reservelijst'
    upsert_record(item)
    moved_message = '"' + item.item_name + '" staat nu op ' + item.item_list
    context.bot.send_message(chat_id=update.effective_chat.id, text=moved_message)


def query_item(command: str, args: set[str]) -> Item:
    list_name = 'Pleepapier'
    if args:
        if '--reserve' in args or '-r' in args:
            list_name = 'Reservelijst'
    session = db_session()
    if command.isdigit():
        remove_index = int(command) - 1
        item = session.query(Item).filter(Item.item_list == list_name).order_by(Item.id).all()[remove_index]
    else:
        item = session.query(Item).filter(Item.item_list == list_name, Item.item_name == command).first()
    session.close()
    return item
