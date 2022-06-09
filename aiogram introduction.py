import pprint

from aiogram import Bot, Dispatcher,executor
from aiogram.types import Message
import asyncio

from parserPhoto import ImageParsing

BOT_TOKEN = "5490426200:AAG4MUqJppCYScZNADDkcmesq52huUxYGXo"
loop = asyncio.get_event_loop()
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot=bot, loop=loop)

@dp.message_handler(commands=['start'])
async def process_start_command(message: Message):
    await message.reply(text = f'Привет, {message.from_user.full_name}')


@dp.message_handler()
async def text_handler(message : Message):
    # if 'отправь фото' in message.text.lower():
    #     await message.answer_photo(photo=)
    # else:
    #     await message.answer(text=message.text)
    # if str(message.text)[:5].lower().strip() == 'image':
    dates = str(message.text).strip()
    impa = ImageParsing(dates)
    pprint.pprint(impa.parse_links())
    photo = impa.download_image(impa.parse_links()[0], "image")
    await message.answer_photo(photo=photo)


executor.start_polling(dp)
