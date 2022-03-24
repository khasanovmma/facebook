from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    print(message)
    await message.answer('<b>Здравствуйте. Поиск групп в Facebook:</b>')
