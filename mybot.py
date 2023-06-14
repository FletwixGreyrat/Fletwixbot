import aiogram
import sqlite3
from create_bot import bot, dp
from handlers import memory, other
from create_bot import db, cursor



memory.memoryHandlers(dp)
other.otherHandlers(dp)


if __name__ == "__main__":
    aiogram.executor.start_polling(skip_updates=True, dispatcher=dp) 