from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from apis import get_random_duck, ask_chat_gpt
from hangman import HangmanGame
from wiki import wiki_page, search_wiki, set_language
from text_to_speech import text_to_speech, speech_to_text
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_TOKEN = '6434503666:AAEz2Kg3h7e_xieY0zwouMpKmA2CzVfK1HM'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
hg = HangmanGame()


@dp.message_handler(commands=['url'])
async def urls(message: types.Message):
  try:
    url_kb = InlineKeyboardMarkup(row_width=1)
    url_kb.add(
            InlineKeyboardButton(text='GitHub', url='https://github.com/m-marika'),
            InlineKeyboardButton(text='Google', url='https://google.com')
        )
    await message.answer('Visit the following links:', reply_markup=url_kb)
  except Exception as e:
    logger.exception("An error occurred in send_url function")  # This logs the stack trace
    await message.answer(f'An error occurred: {e}')

@dp.message_handler(commands=['start'])
async def say_hi(message: types.Message):
  # Функция, отправляющая "Привет" в ответ на команду /start
  try:
    answer = f'Hello, {message.from_user.first_name}!!!'
    await bot.send_message(message.chat.id, answer)
  except Exception as e:
    await message.answer(f'An error occurred: {e}')
    logger.error(f"Error: {e}")


@dp.message_handler(commands=['duck'])
async def duck(message: types.Message):
  try:
    url = get_random_duck()
    await message.answer(url)
  except Exception as e:
    await message.answer('Oops! Something went wrong. Try one more time')
    logger.error(f"Error: {e}")


@dp.message_handler(commands=['GPT'])
async def chat_gpt(message: types.Message):
  try:
    answer = ask_chat_gpt(message.text[4:])
    await message.answer(answer)
  except Exception as e:
    await message.answer('Oops! Something went wrong. Try one more time')
    logger.error(f"Error: {e}")


@dp.message_handler(commands=['setlang'])
async def set_language_command(message: types.Message):
    try:
        lang_code = message.text.split(' ')[1]
        await set_language(lang_code)
        await message.answer(f'Language set to {lang_code}.')
    except Exception as e:
        await message.answer('Failed to set language.')
        logger.error(f"Error: {e}")


@dp.callback_query_handler(lambda call: call.data)
async def answer(call: types.CallbackQuery):
    title, summery, url = await wiki_page(call.data)
    await call.message.answer(call.message.chat.id, text=title)
    await call.message.answer(call.message.chat.id, text=summery)
    await call.message.answer(call.message.chat.id, text=url)


@dp.message_handler(commands=['wiki'])
async def wiki(message: types.Message):
  try:
    text = ' '.join(message.text.split(' ')[1:])
    results = await search_wiki(text)
    markup = InlineKeyboardMarkup()
    buttons = [InlineKeyboardButton(str(res), callback_data=str(res)) for res in results]
    for res in buttons:
        markup.add(res)
    await message.answer('Results: ', reply_markup=markup)
  except Exception as e:
    await message.answer('Sorry, I could not fetch the wiki results.')
    logger.error(f"Error: {e}")


@dp.message_handler()
async def hangman(message: types.Message):
  if hg.game_on:
      if len(message.text) > 1:
          await message.answer("only letter")
          return
      msg = hg.game_step(message.text)
      await message.answer(msg)
      return
  if message.text == 'hangman':
      hg.start()
      text = f'Welcome! Try to win! \n {hg.info()}'
      await message.answer(text)


@dp.message_handler(commands=['speech'])
async def speech(message: types.Message):
  try:
    print('in speech')
    text = ' '.join(message.text.split(' ')[1:])
    print(text)
    text_to_speech(text)
    with open('text_to_speech.mp3', 'rb') as f:
        await message.answer_audio(f)
  except Exception as e:
    logger.exception("An unhandled exception")
    logger.error(f"Error: {e}")


@dp.message_handler(commands=['voice'])
async def voice(message: types.Message):
  try:
    file = bot.get_file(message.voice.file.id)
    bytes = bot.download_file(file.file_path)
    with open('voice.ogg', 'wb') as f:
        f.write(bytes)
    text = speech_to_text()
    await message.answer(text)
  except Exception as e:
    logger.exception("An unhandled exception")
    logger.error(f"Error: {e}")


if __name__ == '__main__':
  try:
    executor.start_polling(dp)
  except Exception as e:
    logger.exception("An unhandled exception")
    logger.error(f"Error: {e}")
