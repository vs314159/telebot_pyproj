from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def inl_keyboard(options:dict) -> InlineKeyboardMarkup:
    buttons = (InlineKeyboardButton(text=opt,  callback_data=call)
               for opt, call in options.items())
    return InlineKeyboardMarkup(row_width=1).add(*buttons)