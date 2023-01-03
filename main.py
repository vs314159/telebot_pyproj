from aiogram import Bot, Dispatcher, executor, types

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

from keyboard import inl_keyboard, get_info

from dotenv import load_dotenv
import os

load_dotenv()

storage = MemoryStorage()
bot = Bot(token=os.environ["TOKEN"])
dp = Dispatcher(bot=bot, storage=storage)


class UserData(StatesGroup):
    name = State()
    contacts = State()


@dp.message_handler(commands=['start'])
async def start(message):
    msg, next_calls, back_opt = get_info('/start')
    inl_kb = inl_keyboard(next_calls, back_opt)
    await message.answer(text=msg, reply_markup=inl_kb)
    await message.delete()


@dp.callback_query_handler(state='*')
async def answer(callback: types.CallbackQuery):
    call = callback.data
    msg, next_calls, back_opt = get_info(call)
    inl_kb = inl_keyboard(next_calls, back_opt)
    await bot.send_message(callback.from_user.id, msg, reply_markup=inl_kb)
    if call == 'auth':
        # проблема після вводу імені - не видаляється пропозиція ввести ім'я
        # стандартні способи видалення повідомлення не працюють
        # коли користувач натискає назад, а потім вводить щось,
        # то бот сприймає це як введене ім'я (І не дивно, адже стан досі .name()
        # потрібно тут логіку трохи переробити
        await UserData.name.set()
    elif call == 'price':
        price_file = 'https://t1.ua/photos/articles/2017/12/10416_1_1097.jpg' # змінити на посилання на ціни
        await bot.send_photo(callback.from_user.id, price_file)
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)#callback.message.delete()


@dp.message_handler(state=UserData.name)
async def name(message, state):
    inp_name = message.text.title()
    await message.delete() # видалити чи не видалити ім_я...
    await state.update_data(name=inp_name)
    await state.finish()
    # пізніше додати превірку чи є таке ім'я в базі
    call = 'auth_done'
    msg, next_calls, back_opt = get_info(call)
    inl_kb = inl_keyboard(next_calls, back_opt)
    await message.answer(msg, reply_markup=inl_kb)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
