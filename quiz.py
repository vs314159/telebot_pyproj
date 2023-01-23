from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor
from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import CallbackQuery
from aiogram.types import Message
from json import dumps
from json import loads
from json import load
import my_db


questions = load(open('questions.json', 'r', encoding='utf-8'))

bot = Bot(token= TOKEN) 
dp = Dispatcher(bot=bot)


def compose_markup(question: int):
    km = InlineKeyboardMarkup(row_width=3)
    for i in range(len(questions[question]["variants"])):
        cd = {
            "question": question,
            "answer": i
        }
        km.insert(InlineKeyboardButton(questions[question]["variants"][i], callback_data=dumps(cd)))
    return km


def reset(uid: int):
    my_db.set_in_process(uid, False)
    my_db.change_questions_passed(uid, 0)
    my_db.change_questions_message(uid, 0)
    my_db.change_current_question(uid, 0)


@dp.callback_query_handler(lambda c: True)
async def answer_handler(callback: CallbackQuery):
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
        await bot.send_message(
            callback.from_user.id,
            f"🎉 Ура, ви пройшли це випробування! \n\n🔒 Ваш рівень англійської - (ще треба прописати). \n✅ Правильних відповідей: {passed} з {len(questions)}."
        )
        return
    await bot.edit_message_text(
        questions[q + 1]["text"],
        callback.from_user.id,
        msg,
        reply_markup=compose_markup(q + 1),
        parse_mode="MarkdownV2"
    )


@dp.message_handler(commands=["play"])
async def go_handler(message: Message):
    if not my_db.is_exists(message.from_user.id):
        my_db.add(message.from_user.id)
    if my_db.is_in_process(message.from_user.id):
        await bot.send_message(message.from_user.id, "🚫 Ви не можете почати тест, тому що *ви вже його проходите*\\.", parse_mode="MarkdownV2")
        return
    my_db.set_in_process(message.from_user.id, True)
    msg = await bot.send_message(
        message.from_user.id,
        questions[0]["text"],
        reply_markup=compose_markup(0),
        parse_mode="MarkdownV2"
    )
    my_db.change_questions_message(message.from_user.id, msg.message_id)
    my_db.change_current_question(message.from_user.id, 0)
    my_db.change_questions_passed(message.from_user.id, 0)

@dp.message_handler(commands=["finish"])
async def quit_handler(message: Message):
    if not my_db.is_in_process(message.from_user.id):
        await bot.send_message(message.from_user.id, "❗️Ви ще не почали тест\\.", parse_mode="MarkdownV2")
        return
    reset(message.from_user.id)
    await bot.send_message(message.from_user.id, "✋🏼 Ви перервали виконання тесту\\.", parse_mode="MarkdownV2")

@dp.message_handler(commands=["start"])
async def start(message: Message):
    await message.answer( "🧠 *Запрошуємо пройти невеликий тест на приблизне визначення рівня англійської*\n\n📝 Потрібно відповісти на 20 питань різного рівня складності\\. \n\n🚨 Результати тесту *НЕ Є 100% відображенням* вашого рівня англійської\\. \n\n👩‍🏫Дуже важливо після тестування пройти speaking частину із викладачем\\. Це допоможе більш точно визначити ваш рівень\\!\n\n*Почати тест* \\- /play\n*Припинити проходження тесту* \\- /finish", parse_mode="MarkdownV2")




def main() -> None:
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()