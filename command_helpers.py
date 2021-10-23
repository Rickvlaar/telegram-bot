import telegram.ext
from util import upsert_records, process_input, delete_records, Command
from data_model import Item, Insult, Kratjes, ItemList, db_session
from datetime import datetime


def get_pleepapier(update: telegram.Update, context: telegram.ext.CallbackContext):
    pleepapier = get_item_list_by_name(list_name='Pleepapier')
    pleepapier = fix_item_postions(item_list=pleepapier)
    pleepapier_string = 'Pleepapier:\n'
    if pleepapier.episode_date:
        pleepapier_string += 'Volgende opname is op ' + pleepapier.list_items.episode_date.strftime('%d-%m-%Y')
    items = [f'{item.item_list_position}. {item.item_name} ({item.created_by})\n' for item in pleepapier.items]
    pleepapier_string = pleepapier_string + ''.join(items)
    context.bot.send_message(chat_id=update.effective_chat.id, text=pleepapier_string)


def add_item(update: telegram.Update, context: telegram.ext.CallbackContext):
    command = process_input(update.message.text)
    list_name = 'Pleepapier'
    if 'reserve' in command.arguments or 'r' in command.arguments:
        list_name = 'Reservelijst'
    items = []
    for command in command.value_list:
        command = command.replace('-r ', '')
        item = Item(item_name=command, item_list=list_name, created_by=update.effective_user.first_name)
        items.append(item)
        input_received_message = '"' + command + '"' + ' staat erop!'
        context.bot.send_message(chat_id=update.effective_chat.id, text=input_received_message)
    upsert_records(items)


def remove_item(update: telegram.Update, context: telegram.ext.CallbackContext):
    command = process_input(update.message.text)
    list_name = 'Pleepapier'
    if 'reserve' in command.arguments or 'r' in command.arguments:
        list_name = 'Reservelijst'
    items = []
    for value in command.value_list:
        value = value.replace('-r ', '')
        item = query_list_item(command=value, list_name=list_name)
        if not item:
            raise ValueError
        items.append(item)
        removed_message = '"' + item.item_name + '" is eraf!'
        context.bot.send_message(chat_id=update.effective_chat.id, text=removed_message)
    delete_records(items)
    item_list = get_item_list_by_name(list_name=list_name)
    fix_item_postions(item_list=item_list)


def move_item(update: telegram.Update, context: telegram.ext.CallbackContext):
    command = process_input(update.message.text)
    list_name = 'Pleepapier'
    if 'reserve' in command.arguments or 'r' in command.arguments:
        list_name = 'Reservelijst'
    items = []
    for value in command.value_list:
        value = value.replace('-r ', '')
        item = query_list_item(command=value, list_name=list_name)
        if not item:
            raise ValueError
        item.item_list = 'Pleepapier' if item.item_list == 'Reservelijst' else 'Reservelijst'
        items.append(item)
        moved_message = '"' + item.item_name + '" staat nu op ' + item.item_list
        context.bot.send_message(chat_id=update.effective_chat.id, text=moved_message)
    upsert_records(items)
    item_list = get_item_list_by_name(list_name=list_name)
    fix_item_postions(item_list=item_list)


def change_item_position(command: Command):
    list_name = 'Pleepapier'
    if 'reserve' in command.arguments or 'r' in command.arguments:
        list_name = 'Reservelijst'
    item_list = get_item_list_by_name(list_name=list_name)

    if 't' in command.arguments or 'target' in command.arguments:
        item_list = position_single_item(command=command, item_list=item_list)
    elif 'a' in command.arguments or 'all' in command.arguments:
        item_list = position_all_items(command=command, item_list=item_list)

    upsert_records(item_list.items)


def position_all_items(command: Command, item_list: ItemList):
    order_argument = command.get_argument(letter_arg='a', word_arg='all')
    order_str = order_argument.value

    if len(order_str) < len(item_list.items) or len(order_str) > 10:
        raise ValueError

    item_position_dict = {item.item_list_position: item for item in item_list.items}
    for index, current_item_pos in enumerate(order_str, 1):
        item = item_position_dict.get(int(current_item_pos))
        item.item_list_position = index

    return item_list


def position_single_item(command: Command, item_list: ItemList):
    moved_item_index = int(command.value)
    target_item_index = int(command.get_argument(letter_arg='t', word_arg='target').value)

    item_position_dict = {item.item_list_position: item for item in item_list.items}
    moved_item = item_position_dict.get(moved_item_index)
    moved_item.item_list_position = target_item_index

    for index, item in item_position_dict.items():
        if target_item_index < moved_item_index and moved_item_index > index >= target_item_index:
            item.item_list_position += 1
        elif target_item_index > moved_item_index and moved_item_index < index <= target_item_index:
            item.item_list_position -= 1

    return item_list


def add_insult(update: telegram.Update, context: telegram.ext.CallbackContext):
    command = process_input(update.message.text)
    items = []
    if len(command.value_list) > 3:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Beetje te veel van het goede gozert')
        return
    for value in command.value_list:
        if len(value) > 140:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text='Jezus lulijzer, hier gelden gewoon twitter regels: max 140 tekens')
            return
        item = Insult(insult=value, created_by=update.effective_user.first_name)
        items.append(item)
    upsert_records(items)
    added_message = 'Goede! Staat erin'
    context.bot.send_message(chat_id=update.effective_chat.id, text=added_message)


def get_kratjes(update: telegram.Update, context: telegram.ext.CallbackContext):
    session = db_session()
    kratjes = session.query(Kratjes).order_by(Kratjes.created_date).all()
    message_text = ''
    for bet in kratjes:
        message_text += f'{bet.better} stelt: '
        bet.due_date = bet.due_date.strftime('%d-%m-%Y') if bet.due_date else 'het einde van dit leven'
        message_text += '"{1}" voor "{2}" met "{0}" als onderpand\n\n'.format(
                bet.stake, bet.bet_description, bet.due_date)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message_text)
    session.close()


def add_bet(update: telegram.Update, context: telegram.ext.CallbackContext):
    command = process_input(update.message.text)
    bet_description = command.value
    better = command.arguments.get('b') if 'b' in command.arguments else command.arguments.get('better')
    stake = command.arguments.get('s') if 's' in command.arguments else command.arguments.get('stake')
    due_date_str = command.arguments.get('d') if 'd' in command.arguments else command.arguments.get('date')

    if better is None or stake is None or due_date_str is None:
        raise ValueError

    due_date = datetime.fromisoformat(due_date_str.value)

    kratje = Kratjes(better=better.value, bet_description=bet_description, stake=stake.value, due_date=due_date)
    upsert_records([kratje])

    message_text = 'De weddenschap is vastgelegd!'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message_text)


def set_next_episode(update: telegram.Update, context: telegram.ext.CallbackContext):
    episode_date_str = update.message.text
    next_episode = datetime.fromisoformat(date_string=episode_date_str)
    session = db_session()
    item_list = session.query(ItemList).filter(ItemList.list_name == 'Pleepapier').first()
    item_list.episode_date = next_episode
    upsert_records(item_list)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'volgende aflevering is op {episode_date_str}')
    session.close()


def query_list_item(command: str, list_name: str) -> Item:
    list_name = list_name
    session = db_session()
    if command.isdigit():
        item_index = int(command)
        item = session.query(Item).filter(Item.item_list == list_name, Item.item_list_position == item_index).first()
    else:
        item = session.query(Item).filter(Item.item_list == list_name, Item.item_name == command).first()
    session.close()
    return item


def get_item_list_by_name(list_name: str) -> ItemList:
    session = db_session()
    item_list = session.query(ItemList) \
        .filter(ItemList.list_name == list_name) \
        .first()
    session.close()
    return item_list


def fix_item_postions(item_list: ItemList) -> ItemList:
    # Items are ordered in the query, so just enumerate all the items and add position
    for index, item in enumerate(item_list.items, 1):
        item.item_list_position = index
    upsert_records([item_list])
    return item_list
