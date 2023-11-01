from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot
from pydub import AudioSegment
import speech_recognition
import os
from apis import get_random_duck, ask_chat_gpt

AudioSegment.converter = "D:/ffmpeg/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe"
AudioSegment.ffmpeg = "D:/ffmpeg/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe"
AudioSegment.ffprobe = "D:/ffmpeg/ffmpeg-master-latest-win64-gpl/bin/ffprobe.exe"


API_TOKEN = '6434503666:AAEz2Kg3h7e_xieY0zwouMpKmA2CzVfK1HM'

bot = telebot.TeleBot(API_TOKEN)
urlKb = InlineKeyboardMarkup(row_width=1)
urlButton = InlineKeyboardButton(text='Blog Skillbox', url='https://skillbox.ru/media/code/')
urlButton2 = InlineKeyboardButton(text='Lesson Skillbox', url='https://skillbox.ru/code/')
urlKb.add(urlButton, urlButton2)


def oga2wav(filename):
    # Конвертация формата файлов
    new_filename = filename.replace('.oga', '.wav')
    audio = AudioSegment.from_file(filename)
    audio.export(new_filename, format='wav')
    return new_filename


def recognize_speech(oga_filename):
    # Перевод голоса в текст + удаление использованных файлов
    wav_filename = oga2wav(oga_filename)
    recognizer = speech_recognition.Recognizer()

    with speech_recognition.WavFile(wav_filename) as source:
        wav_audio = recognizer.record(source)

    text = recognizer.recognize_google(wav_audio, language='ru')

    if os.path.exists(oga_filename):
        os.remove(oga_filename)

    if os.path.exists(wav_filename):
        os.remove(wav_filename)

    return text


def download_file(bot, file_id):
    # Скачивание файла, который прислал пользователь
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    filename = file_id + file_info.file_path
    filename = filename.replace('/', '_')
    with open(filename, 'wb') as f:
        f.write(downloaded_file)
    return filename


@bot.message_handler(commands=['start'])
def say_hi(message):
    # Функция, отправляющая "Привет" в ответ на команду /start
    answer = f'Hello, {message.from_user.first_name}!!!'
    bot.send_message(message.chat.id, text=answer)


@bot.message_handler(commands=['duck'])
def duck(message):
    url = get_random_duck()
    bot.send_message(message.chat.id, text=url)


@bot.message_handler(commands=['GPT'])
def chat_gpt(message):
    answer = ask_chat_gpt(message.text[4:])
    bot.send_message(message.chat.id, text=answer)


@bot.message_handler(content_types=['voice'])
def transcript(message):
    # Функция, отправляющая текст в ответ на голосовое
    filename = download_file(bot, message.voice.file_id)
    text = recognize_speech(filename)
    bot.send_message(message.chat.id, text)


if __name__ == '__main__':
    #executor.start_polling(dp, skip_updates=True)
    bot.polling(non_stop=True)
