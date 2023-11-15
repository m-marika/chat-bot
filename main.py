from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot
from apis import get_random_duck, ask_chat_gpt
from hangman import HangmanGame
from wiki import wiki_page, search_wiki
from text_to_speech import text_to_speech, speech_to_text
import logging

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

API_TOKEN = '6434503666:AAEz2Kg3h7e_xieY0zwouMpKmA2CzVfK1HM'

bot = telebot.TeleBot(API_TOKEN)
hg = HangmanGame()


@bot.message_handler(commands=['url'])
def urls(message):
  try:
    url_kb = InlineKeyboardMarkup(row_width=1)
    url_button1 = InlineKeyboardButton(text='GitHub', url='https://github.com/m-marika')
    url_button2 = InlineKeyboardButton(text='Google', url='https://google.com')
    url_kb.add(url_button1, url_button2)
    bot.send_message(message.chat.id, text='Visit the following links:', reply_markup=url_kb)
  except Exception as e:
    logger.exception("An error occurred in send_url function")  # This logs the stack trace
    bot.reply_to(message, f'An error occurred: {e}')

@bot.message_handler(commands=['start'])
def say_hi(message):
  # Функция, отправляющая "Привет" в ответ на команду /start
  try:
    answer = f'Hello, {message.from_user.first_name}!!!'
    bot.send_message(message.chat.id, text=answer)
  except Exception as e:
    bot.reply_to(message, f'An error occurred: {e}')
    logger.error(f"Error: {e}")


@bot.message_handler(commands=['duck'])
def duck(message):
  try:
    url = get_random_duck()
    bot.send_message(message.chat.id, text=url)
  except Exception as e:
    bot.reply_to(message, 'Oops! Something went wrong. Try one more time')
    logger.error(f"Error: {e}")


@bot.message_handler(commands=['GPT'])
def chat_gpt(message):
  try:
    answer = ask_chat_gpt(message.text[4:])
    bot.send_message(message.chat.id, text=answer)
  except Exception as e:
    bot.reply_to(message, 'Oops! Something went wrong. Try one more time')
    logger.error(f"Error: {e}")


@bot.callback_query_handler(func=lambda call: call.data)
def answer(call):
    title, summery, url = wiki_page(call.data)
    bot.send_message(call.message.chat.id, text=title)
    bot.send_message(call.message.chat.id, text=summery)
    bot.send_message(call.message.chat.id, text=url)


@bot.message_handler(commands=['wiki'])
def wiki(message):
  try:
    text = ' '.join(message.text.split(' ')[1:])
    results = search_wiki(text)
    markup = InlineKeyboardMarkup()
    buttons = [InlineKeyboardButton(str(res), callback_data=str(res)) for res in results]
    for res in buttons:
        markup.add(res)
    bot.send_message(message.chat.id, text='Results: ', reply_markup=markup)
  except Exception as e:
    bot.reply_to(message, 'Sorry, I could not fetch the wiki results.')
    logger.error(f"Error: {e}")


@bot.message_handler()
def hangman(message):
  if hg.game_on:
      if len(message.text) > 1:
          bot.send_message(message.chat.id, text = "only letter")
          return
      msg = hg.game_step(message.text)
      bot.send_message(message.chat.id, text = msg)
      return
  if message.text == 'hangman':
      hg.start()
      text = f'Welcome! Try to win! \n {hg.info()}'
      bot.send_message(message.chat.id, text=text)


@bot.message_handler(commands=['speech'])
def speech(message):
  try:
    print('in speech')
    text = ' '.join(message.text.split(' ')[1:])
    print(text)
    text_to_speech(text)
    with open('text_to_speech.mp3', 'rb') as f:
        bot.send_audio(message.chat.id,f)
  except Exception as e:
    logger.exception("An unhandled exception")
    logger.error(f"Error: {e}")


@bot.message_handler(commands=['voice'])
def voice(message):
  try:
    file = bot.get_file(message.voice.file.id)
    bytes = bot.download_file(file.file_path)
    with open('voice.ogg', 'wb') as f:
        f.write(bytes)
    text = speech_to_text()
    bot.send_message(message.chat.id, text=text)
  except Exception as e:
    logger.exception("An unhandled exception")
    logger.error(f"Error: {e}")


if __name__ == '__main__':
  try:
    bot.polling(non_stop=True)
  except Exception as e:
    logger.exception("An unhandled exception")
    logger.error(f"Error: {e}")
