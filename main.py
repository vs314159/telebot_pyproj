from aiogram import executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import MessageToEditNotFound

from utils.keyboard import inl_keyboard, get_info
from quiz.quiz import go_handler, answer_handler

from setting import bot, dp
from setting import price_files


class UserData(StatesGroup):
    """
    Клас, що необхідний для отримання даних введених у боті користувачем
    name - прізвище та ім'я
    """
    name = State()
    # contacts = State()


async def commands_list_menu(_):
    menu_commands = [types.BotCommand("/start", "Початок роботи бота ▶️"),
                     types.BotCommand("/test_level", "Тест на знання англійської 👨‍🏫"),
                     types.BotCommand("/guest_format", "Вартість і способи навчання 💰"),
                     ]
    await bot.set_my_commands(menu_commands)


@dp.message_handler(commands=['start', 'test_level', 'guest_format'])
async def start(message, state):
    """
    Обробка основних команд

    """
    data = await state.get_data()
    if data.get('chat_id', None):
        try:
            # видаляє інлайн кнопки або можна замінити на
            # видалення попередніх повідомлень з інлайн кнопками
            await bot.edit_message_reply_markup(chat_id=data['chat_id'],
                                                message_id=data['msg_id'],
                                                reply_markup=None)
        except MessageToEditNotFound:
            pass
    await state.finish()
    command = message.text.split()[0][1:]
    msg, next_calls, back_opt = get_info(command)
    inl_kb = inl_keyboard(next_calls, back_opt)
    answ = await message.answer(text=msg, reply_markup=inl_kb)
    # Коли користувач натисне ще одну команду - повідомлення,
    # що надсилалося попередньою командою, позбудеться інлайн кнопок
    await state.update_data(chat_id=answ.chat.id, msg_id=answ.message_id)


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
    prev_call = await state.get_data()
    prev_call = prev_call.get('prev_call', None)
    if '{' not in call:
        back = call.startswith('<')
        call = call.lstrip('<')
        msg, next_calls, back_opt = get_info(call)
        inl_kb = inl_keyboard(next_calls, back_opt)
    else:
        await answer_handler(callback, state)
        return
    if call not in ('price', 'more_prices', 'test_level_start'):
        answ = await bot.send_message(callback.from_user.id, msg, reply_markup=inl_kb)
    match call:
        case 'remains':
            #  Очікування ПІ від користувача, після чого
            #  перехід до функції process_name
            await UserData.name.set()
        case 'student':
            await state.finish()  # користувач не захотів вводити ім'я
        case 'price':
            if len(price_files) in (0, 1):
                inl_kb = inl_keyboard(None, back_opt)  # Прибираємо кнопку '> Далі'
            if len(price_files) > 0:
                photo = price_files[0]
                answ = await bot.send_photo(callback.from_user.id, photo=open(photo, 'rb'), caption=msg, reply_markup=inl_kb)
                await state.update_data(index=len(price_files) > 1)
            else:
                no_prices_msg = 'На жаль, на разі немає зображень з цінами 🥺'  # Якщо папка price_images порожня
                answ = await bot.send_message(callback.from_user.id, no_prices_msg, reply_markup=inl_kb)
        case 'more_prices':
            data = await state.get_data()
            index = data['index']
            if index == len(price_files):
                msg += '(Ви проглянули всі)'
                index = 0
            photo = price_files[index]
            answ = await bot.send_photo(callback.from_user.id, photo=open(photo, 'rb'), caption=msg, reply_markup=inl_kb)
            await state.update_data(index=index + 1)
        case 'test_level_start':
            await go_handler(callback.from_user.id)
    leave_msgs = ('price', 'more_prices', 'guest_solo',
                  'guest_duet', 'guest_group', 'test_level_start',)  # останнє збереже результати test_level_done
    if prev_call in leave_msgs and back:
        await callback.message.edit_reply_markup(None)
    else:
        await callback.message.delete()
    await state.update_data(prev_call=call)
    try:
        await state.update_data(chat_id=answ.chat.id, msg_id=answ.message_id)
    except UnboundLocalError:
        pass


@dp.message_handler(state=UserData.name)
async def process_name(message, state):
    """
    Обробка введеного користувачем прізвища та імені
    """
    inp_name = message.text.title()
    await state.update_data(name=inp_name)
    await state.finish()
    # пізніше додати превірку чи є таке ім'я в базі
    # . . .


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=commands_list_menu)
