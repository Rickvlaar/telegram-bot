import telegram.ext


def krishan(update: telegram.Update, context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Krishan is een luie drol")


def rolf(update: telegram.Update, context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Rolf baft tarrelige anussen")


def steven(update: telegram.Update, context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Steven pijpt drollen")


def add(update: telegram.Update, context: telegram.ext.CallbackContext):
    added_message = ''
    try:
        item_to_add = update.message.text.lstrip('/add').strip().capitalize()
        added_message += '"' + item_to_add + '"' + ' staat erop!'
        pleepapier_file = open('pleepapier.txt', mode='a')
        pleepapier_file.write('\n' + item_to_add)
        pleepapier_file.close()
    except AttributeError:
        added_message = 'retard...'
        pass
    context.bot.send_message(chat_id=update.effective_chat.id, text=added_message)


def pleepapier(update: telegram.Update, context: telegram.ext.CallbackContext):
    pleepapier_file = open('pleepapier.txt').readlines()
    pleepapier_string = 'Pleepapier:\n'
    items = [str(index + 1) + '. ' + item for index, item in enumerate(pleepapier_file)]
    pleepapier_string = pleepapier_string + ''.join(items)
    context.bot.send_message(chat_id=update.effective_chat.id, text=pleepapier_string)


def reservelijst(update: telegram.Update, context: telegram.ext.CallbackContext):
    reservelijst_file = open('reservelijst.txt').readlines()
    reservelijst_string = 'Reservelijst:\n'
    items = [str(index + 1) + '. ' + item for index, item in enumerate(reservelijst_file)]
    reservelijst_string = reservelijst_string + ''.join(items)
    context.bot.send_message(chat_id=update.effective_chat.id, text=reservelijst_string)


def remove(update: telegram.Update, context: telegram.ext.CallbackContext):
    pleepapier_file = open('pleepapier.txt').readlines()
    removed_message = ''
    try:
        index_to_remove = int(update.message.text.lstrip('/remove').strip().capitalize()) - 1
        removed_message += pleepapier_file.pop(index_to_remove) + ' is eraf!'
    except (AttributeError, ValueError, IndexError):
        removed_message += 'Ben je dom ofzo?'
        pass
    new_pleepapier_file = open('pleepapier.txt', mode='w')
    new_pleepapier_file.writelines(pleepapier_file)
    new_pleepapier_file.close()
    context.bot.send_message(chat_id=update.effective_chat.id, text=removed_message)

