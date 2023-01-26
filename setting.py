from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from json import load
from dotenv import load_dotenv
import os
load_dotenv()

storage = MemoryStorage()
bot = Bot(token=os.environ["TOKEN"])#, proxy=os.environ['PROXY_URL'])
dp = Dispatcher(bot=bot, storage=storage)

price_files = os.listdir('price_images')
price_files = tuple(map(lambda x: 'price_images/' + x, price_files))
questions = load(open('questions.json', 'r', encoding='utf-8'))
