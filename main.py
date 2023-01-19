from aiogram import executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State

from keyboard import inl_keyboard, get_info
from quiz import go_handler, answer_handler

from setting import bot, dp
from setting import price_files


class UserData(StatesGroup):
    """
    Клас, що необхідний для отримання даних введених у боті користувачем
    name - прізвище та ім'я
    """
    name = State()
    # contacts = State()


@dp.message_handler(commands=['start'])
async def start(message, state):
    """
    Обробка команди '/start'
    """
    await state.finish()
    msg, next_calls, back_opt = get_info('/start')
    inl_kb = inl_keyboard(next_calls, back_opt)
    await message.answer(text=msg, reply_markup=inl_kb)
    await message.delete()


@dp.message_handler()
async def delete_user_msg(message):
    """
    Видаляємо всі повідомлення, надіслані користувачем
    """
    await message.delete()


@dp.callback_query_handler(state='*')
async def answer(callback: types.CallbackQuery, state):
    """
    Функція, що реагує на колбеки - виводить повідомлення з інлайн-кнопками,
    натискання яких створює нові колбеки, які ця функція знову оброблює
    """
    call = callback.data
    if '{' not in call:
        msg, next_calls, back_opt = get_info(call)
        inl_kb = inl_keyboard(next_calls, back_opt)
    else:
        await answer_handler(callback)
        return

    if call not in ('price', 'more_prices', 'test_level_start'):
        answ = await bot.send_message(callback.from_user.id, msg, reply_markup=inl_kb)
    match call:
        case 'auth':
            #  Очікування ПІ від користувача, після чого
            #  перехід до функції process_name
            await UserData.name.set()
            await state.update_data(chat_id=answ.chat.id, msg_id=answ.message_id)
        case 'student':
            await state.finish()  # користувач не захотів вводити ім'я
        case 'price':
            photo = price_files[0]
            await bot.send_photo(callback.from_user.id, photo=open(photo, 'rb'), caption=msg, reply_markup=inl_kb)
            await state.update_data(index=1)
        case 'more_prices':
            data = await state.get_data()
            index = data['index']
            if index == len(price_files):
                msg += '(Ви проглянули всі)'
                index = 0
            photo = price_files[index]
            await bot.send_photo(callback.from_user.id, photo=open(photo, 'rb'), caption=msg, reply_markup=inl_kb)
            await state.update_data(index=index+1)
        case 'test_level_start':
            await go_handler(callback.from_user.id)
    await callback.message.delete()


@dp.message_handler(state=UserData.name)
async def process_name(message, state):
    """
    Обробка введеного користувачем прізвища та імені
    """
    inp_name = message.text.title()
    await state.update_data(name=inp_name)
    data = await state.get_data()
    await state.finish()
    await bot.delete_message(data['chat_id'], data['msg_id'])
    await message.delete()
    # пізніше додати превірку чи є таке ім'я в базі
    # . . .
    # Створення повідомлення з інлайн-кнопками після успішної авторизації
    call = 'auth_done'
    msg, next_calls, back_opt = get_info(call)
    inl_kb = inl_keyboard(next_calls, back_opt)
    await message.answer(msg + f'{data["name"]}!', reply_markup=inl_kb)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
