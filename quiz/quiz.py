from aiogram.types import CallbackQuery

from json import loads

from setting import dp, bot
from setting import quiz_questions, levels
from utils.keyboard import keyboard, get_info, quiz_keyboard

import quiz.my_db as my_db




def reset(uid: int):
    my_db.set_in_process(uid, False)
    my_db.change_questions_passed(uid, 0)
    my_db.change_questions_message(uid, 0)
    my_db.change_current_question(uid, 0)


@dp.callback_query_handler(lambda c: '{' in c)  # потрібно, щоб не плутати з хендлером в main
async def continue_quiz(callback: CallbackQuery, state):
    data = loads(callback.data)
    q = data["question"]
    is_correct = quiz_questions[q]["correct_answer"] - 1 == data["answer"]
    passed = my_db.get_questions_passed(callback.from_user.id)
    msg = my_db.get_questions_message(callback.from_user.id)
    if is_correct:
        passed += 1
        my_db.change_questions_passed(callback.from_user.id, passed)
    if q + 1 > len(quiz_questions) - 1:
        reset(callback.from_user.id)
        await bot.delete_message(callback.from_user.id, msg)
        msg, next_calls, back_opt = get_info('test_level_done')
        inl_kb = keyboard(next_calls, back_opt)
        lvl_res = levels[passed//len(levels)]
        msg_result = f"🎉 Ваш рівень англійської: {lvl_res}\n\n" \
                     f"✅ Правильних відповідей: {passed} з {len(quiz_questions)}.\n"

        answ = await bot.send_message(
            callback.from_user.id,
            msg_result + msg,
            reply_markup=inl_kb
        )

    else:
        answ = await bot.edit_message_text(
            quiz_questions[q + 1]["text"],
            callback.from_user.id,
            msg,
            reply_markup=quiz_keyboard(q + 1),
            parse_mode="MarkdownV2"
        )
    try:
        await state.update_data(chat_id=answ.chat.id, msg_id=answ.message_id)
    except UnboundLocalError:
        pass


async def start_quiz(user_id):
    reset(user_id) # кожного разу результати тесту анульовуватимуться
    my_db.set_in_process(user_id, True)
    msg = await bot.send_message(
        user_id,
        quiz_questions[0]["text"],
        reply_markup=quiz_keyboard(0),
        parse_mode="MarkdownV2"
    )
    my_db.change_questions_message(user_id, msg.message_id)
    my_db.change_current_question(user_id, 0)
    my_db.change_questions_passed(user_id, 0)
