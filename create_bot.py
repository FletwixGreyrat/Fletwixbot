import asyncio
from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3

storage = MemoryStorage()
# proxy_url = 'http://proxy.server:3128'
# bot = Bot("", proxy=proxy_url)
bot = Bot('')
dp = Dispatcher(bot, storage=storage)
db = sqlite3.connect("Fletwix's DataBase.db")
cursor = db.cursor()
