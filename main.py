from aiogram import Bot, Dispatcher, executor, types

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

from utills import inl_keyboard, get_info

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
        await UserData.name.set()
    await callback.message.delete()


@dp.message_handler(state=UserData.name)
async def name(message, state):
    inp_name = message.text.title()
    await state.update_data(name=name)
    # пізніше додати превірку чи є таке ім'я в базі
    call = 'auth_done'
    msg, next_calls, back_opt = get_info(call)
    inl_kb = inl_keyboard(next_calls, back_opt)
    await message.answer(msg, reply_markup=inl_kb)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
