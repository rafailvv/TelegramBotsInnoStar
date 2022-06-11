from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery
import asyncio
import requests

BOT_TOKEN = "5490426200:AAG4MUqJppCYScZNADDkcmesq52huUxYGXo"

loop = asyncio.get_event_loop()
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot, loop, storage=MemoryStorage())

class Currency(StatesGroup):
    value = State()

@dp.message_handler(commands=['start'])
async def process_start_command(message : Message):
    button = ReplyKeyboardMarkup(resize_keyboard=True)
    button.insert(KeyboardButton(text='в рубли'))
    button.insert(KeyboardButton(text='из рублей'))
    await message.answer('Добро пожаловать!', reply_markup=button)

@dp.message_handler(state=Currency.value)
async def take_value(message : Message, state : FSMContext):
    value = int(message.text)
    data = await state.get_data()

    response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js").json()
    if data['action'] == "В рубли":
        await message.answer(text=value * response['Valute'][data['valute']]['Value']/response['Valute'][data['valute']]['Nominal'])
    elif data['action'] == "из рублей":
        await message.answer(value / (response['Valute'][data['valute']]['Value'] / response['Valute'][data['valute']]['Nominal']))
    await state.reset_state(with_data=False)


@dp.callback_query_handler()
async def change_currency_handler(callback : CallbackQuery, state : FSMContext):
    data = callback.data.split("|")
    if data[0] == "В рубли":
        await state.update_data(valute=data[1])
        await state.update_data(action="В рубли")
        await bot.send_message(chat_id=callback.message.chat.id, text=f"Введи сколько {data[1]} перевести")
        await Currency.value.set()
    elif data[0] == "из рублей":
        await state.update_data(valute=data[1])
        await state.update_data(action="из рублей")
        await bot.send_message(chat_id=callback.message.chat.id, text=f"Введи сколько рублей перевести в {data[1]}")
        await Currency.value.set()


@dp.message_handler()
async def message_handler(message : Message):
    response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js").json()
    all_valute = list(response['Valute'].keys())
    print(all_valute)
    if 'в рубли' in message.text.lower():
        buttons = InlineKeyboardMarkup(row_width=7)
        for i in all_valute:
            buttons.insert(InlineKeyboardButton(text = i, callback_data=f"В рубли|{i}"))
        await message.answer(text="Выберите валюту", reply_markup=buttons)
    elif "из рублей" in message.text.lower():
        buttons = InlineKeyboardMarkup(row_width=7)
        for i in all_valute:
            buttons.insert(InlineKeyboardButton(text=i, callback_data=f"из рублей|{i}"))
        await message.answer(text="Выберите валюту", reply_markup=buttons)


executor.start_polling(dp)