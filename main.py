from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '6434503666:AAEz2Kg3h7e_xieY0zwouMpKmA2CzVfK1HM'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])  # Явно указываем в декораторе, на какую команду реагируем.
async def send_welcome(message: types.Message):
    await message.reply(
        "Привет!\nЯ Эхо-бот!\nОтправь мне любое сообщение, и я его повторю.")  # Так как код работает асинхронно,
    # то обязательно пишем await.


@dp.message_handler()  # Создаём новое событие, которое запускается в ответ на любой текст, введённый пользователем.
async def echo(message: types.Message):
    # Создаём функцию с простой задачей — отправить обратно тот же текст, что ввёл
    # пользователь.
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

