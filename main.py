from typing import Dict

import requests
import aiogram
from aiogram import types
from settings import SiteSettings
from site_API.core import SiteApiInterface
from database.common.models import db, History

bot = aiogram.Bot(token=SiteSettings.telegram_api)


async def start(message: types.Message) -> None:
    await message.reply('Привет! Я бот для покупки авиабилетов.')


async def help(message: types.Message) -> None:
    await message.reply('Список команд:\n'
                        '/low - поиск самых дешевых билетов\n'
                        '/high - поиск самых дорогих билетов\n'
                        '/custom - настройка параметров поиска\n'
                        '/history - история запросов\n'
                        '/help - справка по командам')


async def low(message: types.Message) -> None:
    await message.reply('Поиск самых дешевых билетов')


async def high(message: types.Message) -> None:
    await message.reply('Поиск самых дорогих билетов')


async def custom(message: types.Message) -> None:
    await message.reply('Настройка параметров поиска')


async def history(message: types.Message) -> None:
    chat_id = message.chat.id
    histories = db.session.query(History).filter_by(chat_id=chat_id).all()

    if not histories:
        await message.reply('Вы еще не делали запросов')
        return

    history_text = ''
    for history in histories:
        history_text += f'{history.origin} -> {history.destination} ({history.departure_date})\n'
    await message.reply(history_text)


async def search_tickets(message: types.Message) -> None:
    text = message.text.split()

    if len(text) != 3:
        await message.reply('Для поиска используйте команду /search <город отправления> <город прибытия>')
        return

    origin = text[1]
    destination = text[2]
    departure_date = 'anytime'

    api_interface = SiteApiInterface(api_key=SiteSettings.telegram_api)
    response = api_interface.get_tickets(currency='rub', origin=origin, destination=destination,
                                         departure_date=departure_date)

    if response.status_code != 200:
        await message.reply('Произошла ошибка при поиске')
        return

    tickets = response.json()['data']
    if not tickets:
        await message.reply('По вашему запросу ничего не найдено')
        return

    ticket = tickets[0]
    text = f'🛩 Рейс {ticket["flight_number"]}\n' \
           f'🛫 Вылет: {ticket["depart_date"]} {ticket["depart_time"]}\n' \
           f'🛬 Прилет: {ticket["return_date"]} {ticket["return_time"]}\n' \
           f'💰 Стоимость: {ticket["value"]} рублей\n' \
           f'🌐 Перевозчик: {ticket["gate"]}'
    await message.reply(text)

    chat_id = message.chat.id
    history = History(chat_id=chat_id, origin=origin, destination=destination, departure_date=departure_date)
    db.session.add(history)
    db.session.commit()


async def main():
    dp = aiogram.Dispatcher(bot)


