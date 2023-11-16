import unittest
from unittest.mock import patch, MagicMock
from telebot.types import User, Chat

# Assuming `main` is your bot module with the `say_hi` function
import main

class TestBot(unittest.TestCase):
    @patch('main.bot')
    def test_say_hi(self, mock_bot):
        # Create a User object
        user = User(id=123, is_bot=False, first_name='John', last_name='Doe', username='johndoe')

        # Create a Chat object
        chat = Chat(id=123, type='private')

        # Create a Message object by creating a MagicMock, setting attributes needed
        message = MagicMock(spec=main.telebot.types.Message)
        message.chat = chat
        message.from_user = user
        message.text = '/start'

        # Call the /start command
        main.say_hi(message)

        # Assert that the bot sent the correct message
        mock_bot.send_message.assert_called_with(123, text='Hello, John!!!')

if __name__ == '__main__':
    unittest.main()
