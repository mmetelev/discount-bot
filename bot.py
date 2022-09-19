import os
import json
import logging
from dotenv import load_dotenv, find_dotenv

from aiogram.dispatcher.filters import Text
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hlink, hbold

from parser import get_page_source, get_page_items

load_dotenv(find_dotenv())

API_TOKEN = os.getenv("API_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    start_buttons = ["Кроссовки", "Худи", "Куртки"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Выбери то, что тебе нужно", reply_markup=keyboard)


@dp.message_handler(Text(equals='Кроссовки'))
async def get_discount_sneakers(message: types.Message):
    await message.answer("Ищу самые свежие варианты...")

    get_page_source("https://street-beat.ru/cat/man/obuv/sale/?sort=create&order=desc")
    get_page_items()

    with open("data/data.json", "r", encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        card = f'{hlink(item.get("name"), item.get("url"))}\n' \
               f'Старый прайс: {item.get("old_price")}\n' \
               f'{hbold("Новый прайс: ")} {item.get("new_price")}\n' \
               f'Размеры RU: {item.get("sizes")}'

        await message.answer(card)


@dp.message_handler(Text(equals='Худи'))
async def get_discount_hoodie(message: types.Message):
    await message.answer("Ищу самые свежие варианты...")

    get_page_source("https://street-beat.ru/cat/man/odezhda/tolstovki/sale/?sort=discount&order=desc")
    get_page_items()

    with open("data/data.json", "r", encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        card = f'{hlink(item.get("name"), item.get("url"))}\n' \
               f'Старый прайс: {item.get("old_price")}\n' \
               f'{hbold("Новый прайс: ")} {item.get("new_price")}\n' \
               f'Размеры RU: {item.get("sizes")}'

        await message.answer(card)


@dp.message_handler(Text(equals='Куртки'))
async def get_discount_tshirt(message: types.Message):
    await message.answer("Ищу самые свежие варианты...")

    get_page_source("https://street-beat.ru/cat/man/odezhda/kurtki/sale/?sort=discount&order=desc")
    get_page_items()

    with open("data/data.json", "r", encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        card = f'{hlink(item.get("name"), item.get("url"))}\n' \
               f'Старый прайс: {item.get("old_price")}\n' \
               f'{hbold("Новый прайс: ")} {item.get("new_price")}\n' \
               f'Размеры RU: {item.get("sizes")}'

        await message.answer(card)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
