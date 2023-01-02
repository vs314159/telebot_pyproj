from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from callbacks import callback_info


def inl_keyboard(next_calls=None, back_opt=None) -> InlineKeyboardMarkup:
    options = dict()
    if next_calls is not None:
        options = {nxt_opt: callback_info[nxt_opt] for nxt_opt in next_calls}
    buttons = (InlineKeyboardButton(text=opt.btn_name,
                                    url=opt.url,
                                    callback_data=call)
               for call, opt in options.items())
    kb = InlineKeyboardMarkup(row_width=1).add(*buttons)
    if back_opt is not None:
        kb.add(InlineKeyboardButton(text='< Назад', callback_data=back_opt))
    return kb


def get_info(call):
    info = callback_info[call]
    msg = info.msg
    next_calls = info.next_calls
    back_opt = info.back_opt
    return msg, next_calls, back_opt

