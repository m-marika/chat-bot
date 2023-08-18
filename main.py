from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '6434503666:AAEz2Kg3h7e_xieY0zwouMpKmA2CzVfK1HM'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
urlKb = InlineKeyboardMarkup(row_width=1)
urlButton = InlineKeyboardButton(text='Blog Skillbox', url='https://skillbox.ru/media/code/')
urlButton2 = InlineKeyboardButton(text='Lesson Skillbox', url='https://skillbox.ru/code/')
urlKb.add(urlButton, urlButton2)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Can repeat it?"),
            types.KeyboardButton(text="or this?")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)

    await message.reply("Hello!\nI'm RepeatBot!\nSend me any message and I will repeat it.",
                        reply_markup=keyboard)


@dp.message_handler(commands='url')
async def url_command(message: types.Message):
    await message.answer('Nice web:', reply_markup=urlKb)


@dp.message_handler()  # Создаём новое событие, которое запускается в ответ на любой текст, введённый пользователем.
async def echo(message: types.Message):
    # Создаём функцию с простой задачей — отправить обратно тот же текст, что ввёл
    # пользователь.
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

