import unittest
from unittest.mock import patch, MagicMock
from telebot.types import User, Chat, InlineKeyboardMarkup, InlineKeyboardButton

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


    @patch('main.bot.send_message')
    def test_urls_command(self, mock_send_message):

        message = MagicMock()
        message.chat.id = 123

        with patch('main.InlineKeyboardMarkup') as mock_InlineKeyboardMarkup:
            mock_InlineKeyboardMarkup.return_value = InlineKeyboardMarkup()
            with patch('main.InlineKeyboardButton') as mock_InlineKeyboardButton:
                mock_InlineKeyboardButton.return_value = InlineKeyboardButton(text='GitHub', url='https://github.com/m-marika')
                main.urls(message)

        # Assertions to check if send_message was called with expected arguments
        mock_send_message.assert_called_once()
        args, kwargs = mock_send_message.call_args
        # self.assertEqual(kwargs['chat_id'], 123)
        self.assertEqual(kwargs['text'], 'Visit the following links:')
        self.assertIsInstance(kwargs['reply_markup'], InlineKeyboardMarkup)

        # Check if InlineKeyboardButton was called with expected arguments
        mock_InlineKeyboardButton.assert_any_call(text='GitHub', url='https://github.com/m-marika')
        mock_InlineKeyboardButton.assert_any_call(text='Google', url='https://google.com')


if __name__ == '__main__':
    unittest.main()


