from datetime import datetime, timedelta
import aiogram
import asyncio
import sqlite3
from aiogram import types
from aiogram import Dispatcher, Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from create_bot import db, cursor, dp, bot
# * FSM Классы
class demotivator(StatesGroup):
    photo = State()



#Стартовая команда
# @dp.message_handler(commands=['start'])
async def startCommand(message: types.Message):
    cursor.execute(f"SELECT * FROM money WHERE userId={message.from_user.id}")
    cbbtn1 = InlineKeyboardMarkup().add(InlineKeyboardButton(text='don\'t click this button', url='https://youtu.be/dQw4w9WgXcQ'))
    await message.answer(f'Привет, {message.from_user.first_name}, это бот помощник Fletwix-а. Все полностью защищено, это же Телеграм)))', reply_markup=cbbtn1)
    db.commit()


def otherHandlers(dp: Dispatcher):
    dp.register_message_handler(startCommand, commands=['start'])