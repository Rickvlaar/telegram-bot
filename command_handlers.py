import telegram.ext
import re


def krishan(update: telegram.Update, context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Krishan is een luie drol")


def rolf(update: telegram.Update, context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Rolf baft tarrelige anussen")


def steven(update: telegram.Update, context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Steven pijpt drollen")


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


def add(update: telegram.Update, context: telegram.ext.CallbackContext):
    filename = 'pleepapier.txt'
    added_message = ''
    try:
        item_to_add = update.message.text.lstrip('/add')
        arguments = get_arguments(item_to_add)
        if arguments:
            if '--reserve' in arguments or '-r' in arguments:
                filename = 'reservelijst.txt'
        item_to_add = clean_input(item_to_add, arguments)
        added_message += '"' + item_to_add + '"' + ' staat erop!'
        pleepapier_file = open(filename, mode='a')
        pleepapier_file.write('\n' + item_to_add)
        pleepapier_file.close()
    except AttributeError:
        added_message = 'retard...'
        pass
    context.bot.send_message(chat_id=update.effective_chat.id, text=added_message)


def remove(update: telegram.Update, context: telegram.ext.CallbackContext):
    filename = 'pleepapier.txt'
    removed_message = ''
    try:
        command = update.message.text.lstrip('/remove')
        arguments = get_arguments(command)
        if arguments:
            if '--reserve' in arguments or '-r' in arguments:
                filename = 'reservelijst.txt'
        command = clean_input(command, arguments)
        print(command)
        pleepapier_file = open(filename).readlines()
        removed_message += pleepapier_file.pop(int(command) - 1) + ' is eraf!'
        new_pleepapier_file = open(filename, mode='w')
        new_pleepapier_file.writelines(pleepapier_file)
        new_pleepapier_file.close()
    except (AttributeError, ValueError, TypeError):
        removed_message += 'Ben je dom ofzo?'
        pass
    except IndexError:
        removed_message += 'Dit nummer staat niet op de lijst mongol'
        pass
    context.bot.send_message(chat_id=update.effective_chat.id, text=removed_message)


def get_arguments(command: str) -> set[str]:
    args = set()
    if '--' in command:
        args |= set(re.findall(pattern='([-]{2}\\w*)', string=command))
    if '-' in command:
        args |= set(re.findall(pattern='(-{1}\\w{1}(?![\\w]))', string=command))
    return args


def clean_input(command: str, args: set[str]) -> str:
    if command:
        if args:
            for arg in args:
                command = command.replace(arg, '')
        return command.strip().capitalize()
