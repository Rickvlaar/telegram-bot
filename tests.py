import unittest
from unittest.mock import Mock
import telegram
import telegram.ext
import command_handlers
import command_helpers
from config import Config
from datetime import datetime
from telegram.utils.request import Request


class TestCommandHelpers(unittest.TestCase):

    def test_add_item(self):

        mock_update = Mock()
        mock_update.message.text = '!add test item'
        mock_update.effective_chat.id = 1
        mock_update.effective_user.first_name = 'Henk'

        mock_context = Mock()
        mock_context.bot.send_message()

        command_helpers.add_item(update=mock_update, context=mock_context)
        

if __name__ == '__main__':
    unittest.main()
