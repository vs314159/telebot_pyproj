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


# Видаляємо всі повідомлення, надіслані користувачем
@dp.message_handler()
async def delete_user_msg(message):
    await message.delete()


# змінні для костиля
chat_id, msg_id = None, None


@dp.callback_query_handler(state='*')
async def answer(callback: types.CallbackQuery, state):
    call = callback.data
    msg, next_calls, back_opt = get_info(call)
    inl_kb = inl_keyboard(next_calls, back_opt)
    answ = await bot.send_message(callback.from_user.id, msg, reply_markup=inl_kb)
    match call:
        case 'auth':
            # скоріше це костиль, але поки так можна вмдалити повідомлення
            global chat_id
            chat_id = answ.chat.id
            global msg_id
            msg_id = answ.message_id
            await UserData.name.set()
        case 'student':
            await state.finish()  # користувач не захотів вводити ім'я
        case 'price':
            price_file = 'https://t1.ua/photos/articles/2017/12/10416_1_1097.jpg'  # змінити на посилання на ціни
            await bot.send_photo(callback.from_user.id, price_file)
    await callback.message.delete()


@dp.message_handler(state=UserData.name)
async def name(message, state):
    inp_name = message.text.title()
    await state.update_data(name=inp_name)
    await state.finish()
    await bot.delete_message(chat_id, msg_id)
    await message.delete()
    # пізніше додати превірку чи є таке ім'я в базі
    call = 'auth_done'
    msg, next_calls, back_opt = get_info(call)
    inl_kb = inl_keyboard(next_calls, back_opt)

    await message.answer(msg + f'{inp_name}!', reply_markup=inl_kb)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
