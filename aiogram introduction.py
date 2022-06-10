import pprint
from random import choice

from aiogram import Bot, Dispatcher,executor
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, PollAnswer, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, \
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import asyncio

from parserPhoto import ImageParsing

BOT_TOKEN = "5490426200:AAG4MUqJppCYScZNADDkcmesq52huUxYGXo"
loop = asyncio.get_event_loop()
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot=bot, loop=loop)

@dp.message_handler(commands=['start'])
async def process_start_command(message: Message):
    buttons = ReplyKeyboardMarkup(resize_keyboard=True,row_width=4)
    buttons.insert(KeyboardButton(text="отправь фотку собаки"))
    buttons.insert(KeyboardButton(text="отправь голосовое сообщение"))
    buttons.add(KeyboardButton(text = "отправь локацию"))
    buttons.insert(KeyboardButton(text = "отправь опросник"))
    buttons.add(KeyboardButton(text="стереть данные"))
    await message.reply(text = f'Привет, {message.from_user.full_name}',reply_markup=buttons)


@dp.message_handler(commands=['bye'])
async def process_stop_command(message: Message):
    await message.answer("До свидания!")

@dp.poll_answer_handler()
async def pool_answers(poolAnswer : PollAnswer):
    print(poolAnswer.option_ids, poolAnswer.poll_id)
    print(poolAnswer.get_current())

@dp.callback_query_handler()
async def callback_handler(callback:CallbackQuery):
    data = callback.data
    if data == 'Ответил':
        print(data)
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        await bot.send_message(chat_id=callback.message.chat.id, text = "Спасибо за ответ!")
    else:
        await bot.send_animation(chat_id=callback.message.chat.id, animation="CAACAgIAAxkBAANdYqLpPNgKqhNv_B_hq648Ps6_XA4AAv8BAAIWQmsKSW7R7_hSJA8kBA")

@dp.message_handler()
async def text_handler(message : Message, state : FSMContext):
    await state.update_data(lang = 'ru')
    lang =(await state.get_data())['lang']
    if 'отправь фотку собаки' in message.text.lower():
        dates = str(message.text).strip()
        impa = ImageParsing(dates)
        photo = impa.download_image(choice(impa.parse_links()), "image")
        await message.answer_photo(photo=photo)

    elif 'отправь голосовое сообщение' in message.text.lower():
        await message.answer_voice(voice="AwACAgIAAxkBAAMlYqGxfHxMQLIgqmjQWy0ShJ7XkZgAAm4aAAKWeBFJGRgTgn7tc3gkBA")

    elif 'отправь локацию' in message.text.lower():
        await message.answer_location(latitude=55.753816, longitude=48.743171)
    elif 'отправь опросник' in message.text.lower():
        buttons = InlineKeyboardMarkup()
        buttons.insert(InlineKeyboardButton(text = "Ответил",callback_data="Ответил"))
        buttons.insert(InlineKeyboardButton(text="Не ответил", callback_data="Не ответил"))
        await message.answer_poll(question="Как дела?", options=["Хорошо", "Пойдёт", "Ну такое"], is_anonymous=False,
                                  reply_markup=buttons)
    elif "стереть данные" in message.text.lower():
        await message.answer(text='Данные стерты', reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(text="Я вас не понимаю")
        await asyncio.sleep(20)

executor.start_polling(dp)
