import asyncio
import json

import bs4
import pandas as pd
from aiogram import types

from data.config import sticker_id
from loader import dp, bot, chrome_driver


@dp.message_handler()
async def send_data(message: types.Message):
    list_country = message.text.split()

    for country in list_country:
        number = list_country.index(country) + 1
        await send(country, number, message)
        await asyncio.sleep(600)


async def send(country, number, message: types.Message):
    url = 'https://www.facebook.com/groups/search/groups/?q=' + country

    SESSIONS = await chrome_driver.main_config()

    async with SESSIONS as session:
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
                soup = bs4.BeautifulSoup(html, 'html.parser')
                blocks_div = '.rq0escxv.l9j0dhe7.du4w35lb.hybvsw6c.io0zqebd.m5lcvass.fbipl8qg.nwvqtn77.k4urcfbm.ni8dbmo4.stjgntxs.sbcfpzgs'
                blocks = soup.select(blocks_div)
                title, link, info, count_people, desc, published = [], [], [], [], [], []

                for block in blocks:

                    title.append(block.select_one('.nc684nl6 > a > span').get_text())
                    link.append(block.select_one('.nc684nl6 > a')['href'])
                    if block.select_one(
                            '.d2edcug0.hpfvmrgz.qv66sw1b.c1et5uql.b0tq1wua.e9vueds3.j5wam9gi.b1v8xokw.m9osqain:not(.hzawbc8m)'):
                        if len(block.select_one(
                                '.d2edcug0.hpfvmrgz.qv66sw1b.c1et5uql.b0tq1wua.e9vueds3.j5wam9gi.b1v8xokw.m9osqain:not(.hzawbc8m)').get_text().split(
                            ' · ')) > 1:
                            info.append(block.select_one(
                                '.d2edcug0.hpfvmrgz.qv66sw1b.c1et5uql.b0tq1wua.e9vueds3.j5wam9gi.b1v8xokw.m9osqain:not(.hzawbc8m)').get_text().split(
                                ' · ')[0])
                            count_people.append(block.select_one(
                                '.d2edcug0.hpfvmrgz.qv66sw1b.c1et5uql.b0tq1wua.e9vueds3.j5wam9gi.b1v8xokw.m9osqain:not(.hzawbc8m)').get_text().split(
                                ' · ')[1])
                        elif len(block.select_one(
                                '.d2edcug0.hpfvmrgz.qv66sw1b.c1et5uql.b0tq1wua.e9vueds3.j5wam9gi.b1v8xokw.m9osqain:not(.hzawbc8m)').get_text().split(
                            ' · ')) == 1:
                            info.append(block.select_one(
                                '.d2edcug0.hpfvmrgz.qv66sw1b.c1et5uql.b0tq1wua.e9vueds3.j5wam9gi.b1v8xokw.m9osqain:not(.hzawbc8m)').get_text().split(
                                ' · ')[0])
                            count_people.append('Нет данных')
                    else:
                        info.append('Нет данных')
                        count_people.append('Нет данных')

                    if len(block.select('.jktsbyx5 > span > .a8c37x1j.ni8dbmo4.stjgntxs.l9j0dhe7')) == 1:
                        desc.append('Нет данных')

                    else:
                        try:
                            desc.append(
                                block.select_one(
                                    '.jktsbyx5 > span > .a8c37x1j.ni8dbmo4.stjgntxs.l9j0dhe7').get_text())
                        except Exception as e:
                            desc.append('Нет данных')
                    try:
                        if len(block.select('.jktsbyx5 > span > .a8c37x1j.ni8dbmo4.stjgntxs.l9j0dhe7')) > 1:
                            published.append(
                                block.select('.jktsbyx5 > span > .a8c37x1j.ni8dbmo4.stjgntxs.l9j0dhe7')[
                                    1].get_text())
                        else:
                            if len(block.select_one(
                                    '.jktsbyx5 > span > .a8c37x1j.ni8dbmo4.stjgntxs.l9j0dhe7').get_text()) > 33:
                                index_desc = blocks.index(block)
                                desc[index_desc] = block.select_one(
                                    '.jktsbyx5 > span > .a8c37x1j.ni8dbmo4.stjgntxs.l9j0dhe7').get_text()
                                published.append('Нет данных')
                            else:

                                published.append(
                                    block.select_one(
                                        '.jktsbyx5 > span > .a8c37x1j.ni8dbmo4.stjgntxs.l9j0dhe7').get_text())
                    except Exception as e:
                        published.append('Нет данных')

                excel_file = pd.DataFrame({
                    'Название группы': title,
                    'Ссылка группы': link,
                    'Статус группы': info,
                    'Количество участников': count_people,
                    'Описания группы': desc,
                    'Информация о публикации': published
                })
                excel_file.to_excel(f'{number}){country}.xlsx', sheet_name='information', index=False),

                break

            last_height = new_height

    await message.reply_document(open(f'{number}){country}.xlsx', 'rb'))
