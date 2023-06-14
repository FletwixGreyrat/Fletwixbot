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
import random
from create_bot import db, cursor, dp, bot


#* FSM классы
class delind(StatesGroup):
    answer = State()

class showIndex(StatesGroup):
    index = State()

class load_memory_class(StatesGroup):
    element = State()

#* Загрузка воспоминания
#! @dp.message_handler(commands=['load'], state=None)
async def load_photo(message: types.Message):
    await message.answer("Началась инициализация. Загрузите воспоминание")
    await load_memory_class.element.set()

#! @dp.message_handler(content_types=['photo', 'text'], state=load_memory_class.element)
async def load_memory(message: types.Message, state: FSMContext):
    if message.text == '/nstop':
        await message.answer('Загрузка остановлена')
        await state.finish()
        return
    async with state.proxy() as data:
        if message.photo:
            data['type'] = 'photo'
            data['id'] = message.photo[0].file_id
            if message.caption is None:
                data['text'] = ''
            else:
                data['text'] = message.caption

        elif message.text:  
            data['type'] = 'text'
            data['id'] = 'None'
            data['text'] = message.text

        elif message.video:
            data['type'] = 'video'
            data['id'] = message.video.file_id
            if message.caption is None:
                data['text'] = ''
            else:
                data['text'] = message.caption
    current_datetime = str(datetime.now()).split()[0]
    async with state.proxy() as data:
        cursor.execute(f"INSERT INTO cloud (userId, contentId, textOrCaption, date, dataType) VALUES ('{message.from_user.id}', '{data['id']}', '{data['text']}', '{current_datetime}', '{data['type']}')")
        db.commit()
    await message.answer('Данные успешно загружены!')
    
#! @dp.message_handler(commands=['showlast'])
async def showlast(message: types.Message):
    cursor.execute(F"SELECT * FROM cloud WHERE userId={message.from_user.id}")
    last = cursor.fetchall()
    if last == []:
        await bot.send_message(message.chat.id, text='У вас еще нет соxраненных воспоминаний, вы можете создать их при помощи команды /load')
        return
    last = last[-1]
    if last[4] == "photo":
        await message.answer_photo(photo=last[1], caption=last[2] + '\n' + f'Загружено: {last[3]}')
    elif last[4] == 'video':
        await message.answer_video(video=last[1], caption=last[2] + '\n' + f'Загружено: {last[3]}')
    elif last[4] == 'text':
        await message.answer(text=last[1] + '\n' + f'Загружено: {last[3]}')
#! @dp.message_handler(commands=['showind'], state=None)
async def showall(message: types.Message):
    cursor.execute(f"SELECT * FROM cloud WHERE userId={message.from_user.id}")
    allm = cursor.fetchall()
    counter = 0
    showall_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(len(allm)):
        if counter % 5 != 0:
            showall_keyboard.insert(KeyboardButton(counter + 1))
        else:
            showall_keyboard.add(KeyboardButton(counter + 1))
        counter += 1
    showall_keyboard.add(KeyboardButton('/nstop'))
    if len(allm) == 0:
        await message.answer('У вас еще нет сохраненных восмпоминаний, вы можете создать их с помощью команды /load')
    else:
        await bot.send_message(message.chat.id, text=f'Выберите воспоминания по нажатию кнопки, всего их {len(allm)}. За раз можно перосмотреть сколько угодно воспоминаний, для принудительного выключения напишите /nstop')
        await message.answer('Пожалуйста, выберите воспоминание из выпадающей клавиатуры,', reply_markup=showall_keyboard)
        await showIndex.index.set()
#! @dp.message_handler(content_types=['text'], state=showIndex.index)
async def showindex(message:types.Message, state: FSMContext):
    cursor.execute(f"SELECT * FROM cloud WHERE userId={message.from_user.id}")
    allm = cursor.fetchall()
    if message.text.lower() == '/nstop':
        await message.answer('Выгрузка остановлена')
        await state.finish()
        return
    try:
        indexToSend = int(message.text) - 1
    except:
        await message.answer('Ошибка. Пожалуйста, попробуйте еще раз и введите числовой ответ')
        return
    try:
        memoryToSend = allm[indexToSend]
    except:
        await message.answer('Данных с этим номером нет в списке, используйте числа из выпадающей клавиатуры или команду /nstop. Пожалуйста, попробуйте еще раз.')
    
    if memoryToSend[4] == "photo":
        print(memoryToSend)
        await bot.send_photo(message.chat.id, photo=memoryToSend[1], caption=f'{memoryToSend[2]}\nЗагружено: {memoryToSend[3]}')
    elif memoryToSend[4] == 'video':
        await message.answer_video(video=memoryToSend[1], caption=memoryToSend[2] + '\n' + f'Загружено: {memoryToSend[3]}')
    elif memoryToSend[4] == 'text':
        await message.answer(text=memoryToSend[1] + '\n' + f'Загружено: {memoryToSend[3]}')


#! @dp.message_handler(commands=['delind'], state=None)
async def delind_command(message: types.Message, state: FSMContext):
    cursor.execute(f"SELECT * FROM cloud WHERE userId={message.from_user.id}")
    allm = cursor.fetchall()
    if len(allm) == 0:
        await message.answer('У вас еще нет соxраненных воспоминаний, вы можете создать их при помощи команды /load')
        return
    await message.answer('''Выберите тип удаления и отправьте в соответствии с ним:
1. Удаление промежутка воспоминний
2. Удаление выборочно.
Пропишите порядковый/е номер/а,  в зависимости от выбора.
Пример:
1. 12-15
2. 1 3 5 7
''')
    await delind.answer.set()
#! @dp.message_handler(content_types=['text'], state=delind.answer)
async def delind1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            if '-' in message.text.lower():
                data['conf'] = [int(i) for i in range(int(message.text.split('-')[0]) - 1, int(message.text.split('-')[1]))]
            else:
                data['conf'] = [int(i) - 1 for i in message.text.split()]
        except:
            await message.answer('Ошибка, неправильно введены параметры удаления. ПОпробуйте еще раз.')
            await state.finish()
            return
        cursor.execute(f"SELECT * FROM cloud WHERE userId={message.from_user.id}")
        allm = cursor.fetchall()
        for i in data['conf']:
            try:
                Id = allm[i][1]
                if Id == 'None':
                    Id == allm[i][1]
                cursor.execute(f'DELETE FROM cloud WHERE contentId="{Id}"')
            except:
                await message.answer(f'Воспоминания с номером {i} не существует')
                await state.finish()
                return
        await message.answer('Указанные воспоминания успешно удалены')
        db.commit()
    await state.finish()


def memoryHandlers(dp: Dispatcher):
    dp.register_message_handler(load_photo, commands=['load'], state=None)
    dp.register_message_handler(load_memory, content_types=['photo', 'text', 'video'], state=load_memory_class.element)
    dp.register_message_handler(showlast, commands=['showlast'])
    dp.register_message_handler(showall, commands=['showind'], state=None)
    dp.register_message_handler(showindex, content_types=['text'], state=showIndex.index)
    dp.register_message_handler(delind_command, commands=['delind'], state=None)
    dp.register_message_handler(delind1, content_types=['text'], state=delind.answer)