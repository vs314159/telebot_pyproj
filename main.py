from aiogram import executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import MessageToEditNotFound

from utils.keyboard import keyboard, get_info
from quiz.quiz import start_quiz, continue_quiz

from setting import bot, dp
from setting import price_files, informative_msgs
from setting import number_col, balance_col
from google_integration.num_of_lessons import google_table_df, number_of_lessons_from_sheets


class UserData(StatesGroup):
    """
    Клас, що необхідний для отримання даних введених у боті користувачем
    """
    phone_number = State()


async def commands_list_menu(_):
    menu_commands = [types.BotCommand("/start", "Початок роботи бота ▶️"),
                     types.BotCommand("/test_level", "Тест на знання англійської 👨‍🏫"),
                     types.BotCommand("/guest_format", "Вартість і способи навчання 💰"),
                     ]
    await bot.set_my_commands(menu_commands)


@dp.message_handler(commands=['start', 'test_level', 'guest_format'])
async def command_answer(message, state):
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
    inl_kb = keyboard(next_calls, back_opt)
    answ = await message.answer(text=msg, reply_markup=inl_kb)
    # Коли користувач натисне ще одну команду - попереднє повідомлення,
    # що містило інлайн кнопки
    await state.update_data(chat_id=answ.chat.id, msg_id=answ.message_id)


@dp.message_handler()
async def delete_user_msg(message):
    """
    Видаляє всі повідомлення, надіслані користувачем
    """
    await message.delete()


@dp.callback_query_handler(state='*')
async def answer_callback(callback: types.CallbackQuery, state):
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
        inl_kb = keyboard(next_calls, back_opt)
    else:
        await continue_quiz(callback, state)
        return
    if call not in ('price', 'more_prices', 'test_level_start'):
        answ = await bot.send_message(callback.from_user.id, msg, reply_markup=inl_kb)
    match call:
        case 'remains':
            #  Очікування ПІ від користувача, після чого
            #  перехід до функції process_name
            await UserData.phone_number.set()
            try:
                await state.update_data(chat_id=answ.chat.id, msg_id=answ.message_id)
            except UnboundLocalError:
                pass
        case 'student':
            await state.finish()  # користувач не захотів вводити ім'я
        case 'price':
            if len(price_files) in (0, 1):
                inl_kb = keyboard(None, back_opt)  # Прибираємо кнопку '> Далі'
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
            await start_quiz(callback.from_user.id)
    if prev_call in informative_msgs and back:
        await callback.message.edit_reply_markup(None)
    else:
        await callback.message.delete()
    await state.update_data(prev_call=call)
    try:
        await state.update_data(chat_id=answ.chat.id, msg_id=answ.message_id)
    except UnboundLocalError:
        pass


@dp.message_handler(state=UserData.phone_number)
async def process_phone_number(message, state):
    """
    Обробка введеного користувачем прізвища та імені
    """
    phone_number = message.text
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
    await state.update_data(phone_number=phone_number)
    await state.finish()
    phone_number = phone_number.replace('-', '')
    if check_phone_number_format(phone_number):
        result_msg = number_of_lessons_from_sheets(phone_number,
                                                   google_table_df,
                                                   number_col,
                                                   balance_col)
        if result_msg is None:
            msg, next_calls, back_opt = get_info('remains')
            inl_kb = keyboard(next_calls, back_opt)
            answ = await bot.send_message(message.from_user.id, msg, reply_markup=inl_kb)
            await UserData.phone_number.set()
        else:
            call = 'remains_result'
            msg, next_calls, back_opt = get_info(call)
            msg = result_msg
            inl_kb = keyboard(next_calls, back_opt)
            answ = await bot.send_message(message.from_user.id, msg, reply_markup=inl_kb)
    else:
        msg, next_calls, back_opt = get_info('remains')
        inl_kb = keyboard(next_calls, back_opt)
        answ = await bot.send_message(message.from_user.id, msg, reply_markup=inl_kb)
        await UserData.phone_number.set()
    try:
        await state.update_data(chat_id=answ.chat.id, msg_id=answ.message_id)
    except UnboundLocalError:
        pass



def check_phone_number_format(phone_number):
    phone_number = phone_number.replace('-', '').replace('+', '')
    return len(phone_number) == 12 and \
           phone_number.isnumeric() and \
           phone_number.startswith('380')


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=commands_list_menu)
