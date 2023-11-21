import unittest
from unittest.mock import patch, MagicMock
from telebot.types import User, Chat, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

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


  @patch('main.get_random_duck', return_value='http://random-duck-url.com')
  @patch('main.bot')
  def test_duck_success(self, mock_bot, mock_get_random_duck):
    # Create a fake Message object
    chat = MagicMock()
    chat.id = 123
    message = MagicMock()
    message.chat = chat

    main.duck(message)

    # Assert get_random_duck was called
    mock_get_random_duck.assert_called_once()

    # Assert bot sent the correct message
    mock_bot.send_message.assert_called_once_with(123, text='http://random-duck-url.com')


  @patch('main.get_random_duck', side_effect=Exception('Test exception'))
  @patch('main.bot')
  @patch('main.logger')
  def test_duck_failure(self, mock_logger, mock_bot, mock_get_random_duck):
    # Create a fake Message object
    chat = MagicMock()
    chat.id = 123
    message = MagicMock()
    message.chat = chat

    main.duck(message)

    # Assert bot sent the error message
    mock_bot.reply_to.assert_called_once_with(message, 'Oops! Something went wrong. Try one more time')

    # Assert the exception was logged
    mock_logger.error.assert_called_once_with('Error: Test exception')


  @patch('main.bot')
  @patch('main.wiki_page', return_value=('Title', 'Summary', 'URL'))
  def test_answer(self, wiki_page_mock, bot_mock):
    # Create a mock CallbackQuery object
    call = MagicMock(spec=CallbackQuery)
    call.data = 'query data'
    call.message = MagicMock()
    call.message.chat = MagicMock()
    call.message.chat.id = 123

    main.answer(call)

    # Assertions to ensure wiki_page is called and messages are sent
    wiki_page_mock.assert_called_once_with(call.data)
    bot_mock.send_message.assert_any_call(123, text='Title')
    bot_mock.send_message.assert_any_call(123, text='Summary')
    bot_mock.send_message.assert_any_call(123, text='URL')

  @patch('main.bot')
  @patch('main.search_wiki', return_value=['Result1', 'Result2'])
  def test_wiki(self, search_wiki_mock, bot_mock):
    # Create a mock Message object
    message = MagicMock(spec=main.telebot.types.Message)
    message.text = '/wiki search_term'
    message.chat = MagicMock()
    message.chat.id = 123

    main.wiki(message)

    # Assertions to check the correct methods are called
    search_wiki_mock.assert_called_once_with('search_term')
    bot_mock.send_message.assert_called_once()

    # Verify that the markup is constructed properly
    args, kwargs = bot_mock.send_message.call_args
    markup = kwargs['reply_markup']
    self.assertIsInstance(markup, InlineKeyboardMarkup)
    self.assertEqual(len(markup.keyboard), 2)  # Assuming there are 2 results
    for button in markup.keyboard:
        self.assertIsInstance(button[0], InlineKeyboardButton)

if __name__ == '__main__':
    unittest.main()


