import asyncio
import json
from aiogram import types
from arsenic import keys

from loader import dp, bot, chrome_driver


@dp.message_handler(commands='cookie')
async def send_data(message: types.Message):
    SESSIONS = await chrome_driver.main_config()
    try:
        async with SESSIONS as session:
            await session.get('https://www.facebook.com/')
            await asyncio.sleep(5)
            login = await session.wait_for_element(5, 'input[name=email]')
            password = await session.wait_for_element(5, 'input[name=pass]')
            await login.send_keys('khasanovmma702@gmail.com')
            await password.send_keys('A65165199a')
            await password.send_keys(keys.ENTER)
            await asyncio.sleep(10)
            data = await session.get_all_cookies()
            with open('cookies.json', 'w') as file:
                json.dump(data, file)
        await message.reply('done')
    except Exception as e:
        await message.reply(f'Error: {e.__class__.__name__}: {e}')