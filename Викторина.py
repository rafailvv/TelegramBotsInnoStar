import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

BOT_TOKEN = "5490426200:AAG4MUqJppCYScZNADDkcmesq52huUxYGXo"

loop = asyncio.get_event_loop()
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot, loop, storage=MemoryStorage())

class QuizAnswers(StatesGroup):
    none_answer = State()
    dont_know = State()

@dp.message_handler(state=QuizAnswers.none_answer)
async def first_ques(message : Message, state : FSMContext):
    # data = await state.get_data()
    if message.text == "None":
        # await state.update_data(correct = data['correct'] + 1)
        async with state.proxy() as data:
            data['correct'] += 1
    await message.answer("Второй вопрос: Ок или не ок?")
    await QuizAnswers.dont_know.set()

@dp.message_handler(state=QuizAnswers.dont_know)
async def second_ques(message : Message, state : FSMContext):
    if message.text == 'ок':
        async with state.proxy() as data:
            data['correct'] += 1
            await message.answer(f"Tест окончен! Правильных ответов {data['correct']}/2")
    await state.finish()

@dp.message_handler(commands=["startquiz"])
async def start_quiz(message : Message, state : FSMContext):
    await message.answer("Викторина на тему \"Программирования\" начилась!")
    buttons = ReplyKeyboardMarkup(resize_keyboard=True,row_width=4)
    buttons.insert(KeyboardButton(text="int"))
    buttons.insert(KeyboardButton(text="None"))
    buttons.insert(KeyboardButton(text="null"))
    buttons.insert(KeyboardButton(text="не знаю"))
    await message.answer("Первый вопрос: Что такое неопределённый тип данных в Python?",
                         reply_markup=buttons)
    await state.update_data(correct = 0)
    await QuizAnswers.none_answer.set()


executor.start_polling(dp)