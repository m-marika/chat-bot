import unittest
from unittest.mock import patch, AsyncMock, mock_open, MagicMock, ANY
from telebot.types import User, Chat, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import asyncio
import main
from hangman import HangmanGame

class TestBot(unittest.IsolatedAsyncioTestCase):

  @patch('main.bot.send_message', new_callable=AsyncMock)
  async def test_say_hi(self, mock_send_message):
    user = User(id=123, is_bot=False, first_name='John', last_name='Doe', username='johndoe')
    chat = Chat(id=123, type='private')
    message = AsyncMock()
    message.chat = chat
    message.from_user = user
    message.text = '/start'

    await main.say_hi(message)

    mock_send_message.assert_called_with(123, 'Hello, John!!!')


  @patch('main.bot', new_callable=AsyncMock)
  async def test_start_command_error(self, mock_send_message):
    message = AsyncMock()
    message.chat.id = 123
    message.from_user.first_name = 'John'
    message.answer = AsyncMock()

    with patch('main.say_hi', side_effect=Exception('Test start exception')):
        await main.say_hi(message)

    print(mock_send_message.mock_calls)

    message.answer.assert_called_once_with('An error occurred: Test start exception')

  @patch('main.bot.send_message', new_callable=AsyncMock)
  async def test_urls_command(self, mock_send_message):
    message = AsyncMock()
    message.chat.id = 123

    await main.urls(message)

    mock_send_message.assert_called_once()
    args, kwargs = mock_send_message.call_args

    self.assertEqual(kwargs['text'], 'Visit the following links:')
    self.assertIsInstance(kwargs['reply_markup'], InlineKeyboardMarkup)

    # Check if the reply_markup contains the correct buttons
    buttons = kwargs['reply_markup'].inline_keyboard
    self.assertTrue(any(btn.text == 'GitHub' for btn in buttons[0]))
    self.assertTrue(any(btn.text == 'Google' for btn in buttons[1]))


  @patch('main.get_random_duck', return_value='http://random-duck-url.com')
  @patch('main.bot', new_callable=AsyncMock)
  async def test_duck_success(self, mock_bot, mock_get_random_duck):
    # Create a fake Message object
    message = AsyncMock()
    message.chat.id = 123

    await main.duck(message)

    # Assert get_random_duck was called
    mock_get_random_duck.assert_called_once()
    mock_bot.send_message.assert_called_once_with(123, text='http://random-duck-url.com')


  @patch('main.get_random_duck', side_effect=Exception('Test exception'))
  @patch('main.bot', new_callable=AsyncMock)
  @patch('main.logger')
  async def test_duck_failure(self, mock_logger, mock_bot, mock_get_random_duck):
    # Create a fake Message object
    chat = AsyncMock()
    chat.id = 123
    message = AsyncMock()

    await main.duck(message)

    # Assert bot sent the error message
    mock_bot.reply_to.assert_called_once_with(message, 'Oops! Something went wrong. Try one more time')

    # Assert the exception was logged
    mock_logger.error.assert_called_once_with('Error: Test exception')


  @patch('main.bot', new_callable=AsyncMock)
  @patch('main.wiki_page', return_value=('Title', 'Summary', 'URL'))
  async def test_answer(self, wiki_page_mock, bot_mock):
    # Create a mock CallbackQuery object
    call = AsyncMock(spec=CallbackQuery)
    call.data = 'query data'
    call.message = AsyncMock()
    call.message.chat = AsyncMock()
    call.message.chat.id = 123

    await main.answer(call)

    # Assertions to ensure wiki_page is called and messages are sent
    wiki_page_mock.assert_called_once_with(call.data)
    bot_mock.send_message.assert_has_calls([
        call(123, text='Title'),
        call(123, text='Summary'),
        call(123, text='URL')
    ])

  @patch('main.bot')
  @patch('main.search_wiki', return_value=['Result1', 'Result2'])
  async def test_wiki(self, search_wiki_mock, bot_mock):
    # Create a mock Message object
    message = AsyncMock()
    message.text = '/wiki search_term'
    message.answer = AsyncMock()
    message.chat.id = 123

    await main.wiki(message)

    # Assertions to check the correct methods are called
    search_wiki_mock.assert_called_once_with('search_term')
    bot_mock.answer.assert_called_once_with('Results: ', reply_markup=ANY)
    # bot_mock.send_message.assert_called_once()

    # # Verify that the markup is constructed properly
    # args, kwargs = bot_mock.send_message.call_args
    # markup = kwargs['reply_markup']
    # self.assertIsInstance(markup, InlineKeyboardMarkup)
    # self.assertEqual(len(markup.keyboard), 2)  # Assuming there are 2 results
    # for button in markup.keyboard:
    #     self.assertIsInstance(button[0], InlineKeyboardButton)


  @patch('main.bot', new_callable=AsyncMock)
  @patch('main.ask_chat_gpt', side_effect=Exception('Test GPT exception'))
  async def test_gpt_command_error(self, mock_ask_chat_gpt, mock_bot):
      # Mock a message object with necessary attributes
      message = AsyncMock()
      message.text = '/GPT ask something'
      message.chat.id = 123
      message.answer = AsyncMock()

      await main.chat_gpt(message)

      mock_bot.reply_to.assert_called_once_with(message, 'Oops! Something went wrong. Try one more time')


  @patch('main.bot', new_callable=AsyncMock)
  async def test_set_language_command_success(self, mock_bot):
      # Mock a message object with necessary attributes
      message = AsyncMock()
      message.text = '/setlang en'
      message.chat.id = 123

      # Simulate setting language success
      with patch('main.set_language', return_value=True):
          await main.set_language_command(message)

      # Assert bot sent confirmation message
      mock_bot.send_message.assert_called_once_with(123, 'Language set to en.')

  @patch('main.bot', new_callable=AsyncMock)
  async def test_hangman_start(self, mock_bot):
      # Mock a message object with necessary attributes
      message = AsyncMock()
      message.text = 'hangman'
      message.chat.id = 123

      mock_hg = MagicMock()
      main.hg = mock_hg
      main.hg.info.return_value = 'Game Info'

      await main.hangman(message)

      mock_hg.start.assert_called_once()
      mock_bot.send_message.assert_called_once_with(123, text='Welcome! Try to win! \n Game Info')


  @patch('main.bot', new_callable=AsyncMock)
  async def test_hangman_guess(self, mock_bot):
      # Mock a message object with necessary attributes
      message = AsyncMock()
      message.text = 'a'
      message.chat.id = 123
      main.hg.game_on = True

      mock_hg = MagicMock()
      main.hg = mock_hg
      main.hg.game_step.return_value = 'Some game step response'

      await main.hangman(message)

      mock_hg.game_step.assert_called_once_with('a')
      mock_bot.send_message.assert_called_once_with(123, text='Some game step response')


  @patch('main.bot', new_callable=AsyncMock)
  async def test_speech_command(self, mock_bot):
      # Mock a message object with necessary attributes
      message = AsyncMock()
      message.text = '/speech Hello'
      message.chat.id = 123

      # Simulate text_to_speech function and file opening
      with patch('main.text_to_speech') as mock_text_to_speech, \
          patch('builtins.open', mock_open(read_data='audio data')) as mock_file:
          await main.speech(message)

      mock_text_to_speech.assert_called_once_with('Hello')

      # Assert bot sent the audio message
      mock_bot.send_audio.assert_called_once()


if __name__ == '__main__':
    unittest.main()


