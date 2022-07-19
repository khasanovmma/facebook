import asyncio
import json
import os

import bs4
import pandas as pd
from aiogram import types

from data.config import wait_sticker_id, done_sticker_id, ADMINS, BASE_DIR
from loader import dp, bot, chrome_driver


@dp.message_handler()
async def send_data(message: types.Message):
    list_country = message.text.split('\n')
    await bot.send_message(ADMINS[0], message.text + '\n\n' + message.from_user.username if message.from_user.username else 'None')
    sticker_msg = await message.answer_sticker(wait_sticker_id)
    msg = await message.answer('Пожалуйста подождите😊. Уведомлю когда все закончится.')
    for country in list_country:
        number = list_country.index(country) + 1
        send(country, number, message)
        if not number == len(list_country):
            await asyncio.sleep(600)

    await message.answer_sticker(done_sticker_id)
    await sticker_msg.delete()
    await msg.delete()
    await message.reply('Список пройден ✅✅✅')
    await bot.send_message(ADMINS[0], 'Список пройден ✅✅✅')


def send(country, number, message: types.Message):
    url = 'https://www.facebook.com/groups/search/groups/?q=' + country

    SESSIONS = await chrome_driver.main_config()
    try:
        async with SESSIONS as session:
            await asyncio.sleep(3)
            await session.get("https://www.facebook.com/")
            await asyncio.sleep(3)

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

                    await asyncio.sleep(5)

                    soup = bs4.BeautifulSoup(html, 'html.parser')
                    blocks_div = '.d2edcug0.o7dlgrpb > .sjgh65i0'
                    blocks = soup.select(blocks_div)

                    title, link, info, count_people, desc, published = [], [], [], [], [], []
                    div_title = '.oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.nc684nl6.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.gpro0wi8.oo9gr5id.lrazzd5p'
                    div_info_count_people_last_public = '.d9wwppkn.hrzyx87i.jq4qci2q.a3bd9o3v.b1v8xokw > span'
                    div_desc = '.tia6h79c.iv3no6db.e9vueds3.j5wam9gi.b1v8xokw'

                    for block in blocks:
                        title.append(block.select_one(div_title).get_text())
                        link.append(block.select_one(div_title)['href'])
                        if block.select_one(div_info_count_people_last_public):
                            if len(block.select_one(div_info_count_people_last_public).get_text().split(' · ')) > 1:
                                info.append(block.select_one(div_info_count_people_last_public).get_text().split(' · ')[0])
                                count_people.append(
                                    block.select_one(div_info_count_people_last_public).get_text().split(' · ')[1])
                                try:
                                    published.append(
                                        block.select_one(div_info_count_people_last_public).get_text().split(' · ')[2])
                                except Exception as e:
                                    published.append('Нет данных')
                            elif len(block.select_one(div_info_count_people_last_public).get_text().split(' · ')) == 1:
                                info.append(block.select_one(div_info_count_people_last_public).get_text().split(' · ')[0])
                                count_people.append('Нет данных')
                                published.append('Нет данных')
                        else:
                            info.append('Нет данных')
                            count_people.append('Нет данных')
                            published.append('Нет данных')

                        try:
                            if block.select_one(div_desc):
                                desc.append(block.select_one(div_desc).get_text())
                            else:
                                desc.append('Нет данных')
                        except Exception as e:
                            desc.append('Нет данных')

                    excel_file = pd.DataFrame({
                        'Название группы': title,
                        'Ссылка группы': link,
                        'Статус группы': info,
                        'Количество участников': count_people,
                        'Описания группы': desc,
                        'Информация о публикации': published
                    })
                    excel_file.to_excel(f'{number}){country}.xlsx', sheet_name='information',
                                        index=False),

                    break

                last_height = new_height

        await message.reply_document(open(f'{BASE_DIR}/{number}){country}.xlsx', 'rb'))
        await asyncio.sleep(5)
        os.remove(f'{BASE_DIR}/{number}){country}.xlsx')
    except Exception as e:
        await session.close()
        await message.answer('Что то пошло не так 🛑🛑🛑')
        print(e)
