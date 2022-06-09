import pprint
from random import choice

from aiogram import Bot, Dispatcher,executor
from aiogram.types import Message, PollAnswer
import asyncio

from parserPhoto import ImageParsing

BOT_TOKEN = "5490426200:AAG4MUqJppCYScZNADDkcmesq52huUxYGXo"
loop = asyncio.get_event_loop()
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot=bot, loop=loop)

@dp.message_handler(commands=['start'])
async def process_start_command(message: Message):
    await message.reply(text = f'Привет, {message.from_user.full_name}')

@dp.poll_answer_handler()
async def pool_answers(poolAnswer : PollAnswer):
    print(poolAnswer.option_ids, poolAnswer.poll_id)
    print(poolAnswer.get_current())

@dp.message_handler()
async def text_handler(message : Message):
    # Отправляет фотку по запросу
    # dates = str(message.text).strip()
    # impa = ImageParsing(dates)
    # photo = impa.download_image(choice(impa.parse_links()), "image")
    # await message.answer_photo(photo=photo)
    # await bot.send_message(chat_id=, text=)

    # await message.answer_voice(voice="AwACAgIAAxkBAAMlYqGxfHxMQLIgqmjQWy0ShJ7XkZgAAm4aAAKWeBFJGRgTgn7tc3gkBA")


    # await message.answer_location(latitude=55.753816, longitude=48.743171)

    await message.answer_poll(question="Как дела?", options=["Хорошо", "Пойдёт", "Ну такое"], is_anonymous=False)


executor.start_polling(dp)
