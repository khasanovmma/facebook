import asyncio
import json

import bs4
import pandas as pd
from aiogram import types

from data.config import sticker_id
from loader import dp, bot, chrome_driver


@dp.message_handler()
async def send_data(message: types.Message):
    url = message.text
    chat_id = message.from_user.id
    message_id = message.message_id + 1
    message_id_2 = message.message_id + 2

    await message.answer_sticker(sticker_id)
    await message.answer('Пожалуйста подождите😊. Это займет пару минут ⏱.')
    SESSIONS = await chrome_driver.main_config()

    try:
        async with SESSIONS as session:
            await session.get(url)
            await asyncio.sleep(2)

            with open('cookies.json') as file:
                data = json.load(file)
                for item in data:
                    await session.add_cookie(name=item['name'],
                                             value=item['value'],
                                             path=item['path'],
                                             domain=item['domain'],
                                             secure=item['secure'],
                                             httponly=item['httpOnly'])

            await session.get(url)
            await asyncio.sleep(10)

            last_height = session.execute_script("return document.body.scrollHeight")

            while True:

                await session.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                await asyncio.sleep(3)

                new_height = await session.execute_script("return document.body.scrollHeight")

                if new_height == last_height:

                    html = await session.get_page_source()
                    soup = bs4.BeautifulSoup(html, 'html.parser')
                    blocks_div = '.rq0escxv.l9j0dhe7.du4w35lb.hybvsw6c.io0zqebd.m5lcvass.fbipl8qg.nwvqtn77.k4urcfbm.ni8dbmo4.stjgntxs.sbcfpzgs'
                    blocks = soup.select(blocks_div)
                    title, link, info, count_people, desc, published = [], [], [], [], [], []

                    for block in blocks:
                        title.append(block.select_one('.nc684nl6 > a > span').get_text())
                        link.append(block.select_one('.nc684nl6 > a')['href'])
                        info.append(block.select_one(
                            '.d2edcug0.hpfvmrgz.qv66sw1b.c1et5uql.lr9zc1uh.e9vueds3.j5wam9gi.b1v8xokw.m9osqain:not(.hzawbc8m)').get_text().split(
                            ' · ')[0])
                        count_people.append(block.select_one(
                            '.d2edcug0.hpfvmrgz.qv66sw1b.c1et5uql.lr9zc1uh.e9vueds3.j5wam9gi.b1v8xokw.m9osqain:not(.hzawbc8m)').get_text().split(
                            ' · ')[1])

                        desc.append(block.select_one(
                            '.jktsbyx5 > span > .a8c37x1j.ni8dbmo4.stjgntxs.l9j0dhe7').get_text())
                        if len(block.select('.jktsbyx5 > span > .a8c37x1j.ni8dbmo4.stjgntxs.l9j0dhe7')) > 1:
                            published.append(
                                block.select('.jktsbyx5 > span > .a8c37x1j.ni8dbmo4.stjgntxs.l9j0dhe7')[
                                    1].get_text())
                        else:
                            published.append('Нет данных')
                    excel_file = pd.DataFrame({
                        'Название группы': title,
                        'Ссылка группы': link,
                        'Количество участников': count_people,
                        'Описания группы': desc,
                        'Информация о публикации': published
                    })
                    excel_file.to_excel('information.xlsx', sheet_name='information', index=False),

                    break

                last_height = new_height

        await bot.delete_message(chat_id, message_id)
        await bot.delete_message(chat_id, message_id_2)

        await message.reply_document(open('information.xlsx', 'rb'))

    except Exception as ex:
        await bot.delete_message(chat_id, message_id)
        await bot.delete_message(chat_id, message_id_2)

        await message.answer('Что то пошло не так 🛑🛑🛑')
        print(ex)
