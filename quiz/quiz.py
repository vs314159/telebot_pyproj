from aiogram.types import CallbackQuery

from json import loads

from setting import dp, bot
from setting import questions
from utils.keyboard import inl_keyboard, get_info, compose_markup

import quiz.my_db as my_db

levels = ['Elementary', 'Pre-Intermediate', 'Intermediate', 'Upper-Intermediate']


def reset(uid: int):
    my_db.set_in_process(uid, False)
    my_db.change_questions_passed(uid, 0)
    my_db.change_questions_message(uid, 0)
    my_db.change_current_question(uid, 0)


@dp.callback_query_handler(lambda c: '{' in c)  # потрібно, щоб не плутати з хендлером в main
async def answer_handler(callback: CallbackQuery, state):
    data = loads(callback.data)
    q = data["question"]
    is_correct = questions[q]["correct_answer"] - 1 == data["answer"]
    passed = my_db.get_questions_passed(callback.from_user.id)
    msg = my_db.get_questions_message(callback.from_user.id)
    if is_correct:
        passed += 1
        my_db.change_questions_passed(callback.from_user.id, passed)
    if q + 1 > len(questions) - 1:
        reset(callback.from_user.id)
        await bot.delete_message(callback.from_user.id, msg)
        ## додаю клавіатуру
        msg, next_calls, back_opt = get_info('test_level_done')
        inl_kb = inl_keyboard(next_calls, back_opt)
        lvl_res = levels[passed//len(levels)]
        msg_result = f"🎉 Ваш рівень англійської: {lvl_res}\n\n" \
                     f"\n✅ Правильних відповідей: {passed} з {len(questions)}.\n"

        ####
        answ = await bot.send_message(
            callback.from_user.id,
            msg_result + '\n' + msg,
            reply_markup=inl_kb
        )

    else:
        answ = await bot.edit_message_text(
            questions[q + 1]["text"],
            callback.from_user.id,
            msg,
            reply_markup=compose_markup(q + 1),
            parse_mode="MarkdownV2"
        )
    try:
        await state.update_data(chat_id=answ.chat.id, msg_id=answ.message_id)
    except UnboundLocalError:
        pass


async def go_handler(user_id):
    reset(user_id) # кожного разу результати тесту анульовуватимуться
    my_db.set_in_process(user_id, True)
    msg = await bot.send_message(
        user_id,
        questions[0]["text"],
        reply_markup=compose_markup(0),
        parse_mode="MarkdownV2"
    )
    my_db.change_questions_message(user_id, msg.message_id)
    my_db.change_current_question(user_id, 0)
    my_db.change_questions_passed(user_id, 0)
