from aiogram import Bot, Dispatcher, executor, types

from dotenv import load_dotenv
import os
load_dotenv()

from utills.keyboard import inl_keyboard
from text.relations import relations, info_dict

bot = Bot(token=os.environ["TOKEN"])
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(inp):
    msg = info_dict['/start'].message
    options = {info_dict[nxt_opt].btn_name: nxt_opt for nxt_opt in relations['/start']}
    start_kb = inl_keyboard(options)
    await inp.answer(msg, reply_markup=start_kb)

@dp.callback_query_handler()
async def answer(callback: types.CallbackQuery):
    call = callback.data
    msg = info_dict.get(call) # !
    next_calls = relations.get(call)
    msg = msg.message # !
    if next_calls is not None:
        options = {info_dict[nxt_opt].btn_name: nxt_opt for nxt_opt in next_calls}
        inl_kb = inl_keyboard(options)
        await bot.send_message(callback.from_user.id, msg, reply_markup=inl_kb)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)