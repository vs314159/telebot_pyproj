from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from json import load
from dotenv import load_dotenv
import os
load_dotenv()

storage = MemoryStorage()
bot = Bot(token=os.environ["TOKEN"], proxy=os.environ['PROXY_URL'])
# якщо не працюватиме proxy - закоментити
dp = Dispatcher(bot=bot, storage=storage)

price_files = os.listdir('price_images')
price_files = tuple(map(lambda x: 'price_images/' + x, price_files))
quiz_questions = load(open('quiz/questions.json', 'r', encoding='utf-8'))
my_db_file = 'quiz/my_bot.db'
informative_msgs = (
                    'price', 'more_prices', 'guest_solo',
                    'guest_duet', 'guest_group', 'test_level_start',
                    )
levels = [
          'Elementary', 'Pre-Intermediate',
          'Intermediate', 'Upper-Intermediate',
          ]
prices = {
            'solo': 3000,
            'duet': 2200,
            'group': 1950,
         }

google_table_id = os.environ['GOOGLE_TABLE_ID']
number_col = 'номер телефону'
balance_col = 'баланс уроков'
