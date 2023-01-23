from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from callbacks import callback_info
from json import dumps, load


questions = load(open('questions.json', 'r', encoding='utf-8'))


# SandyGrN's function
def compose_markup(question: int):
    """
    Інлайн-клавіатура для тесту з англійської з кнопками варіантів відповіді
    """
    km = InlineKeyboardMarkup(row_width=3)
    for i in range(len(questions[question]["variants"])):
        cd = {
            "question": question,
            "answer": i
        }
        km.insert(InlineKeyboardButton(questions[question]["variants"][i], callback_data=dumps(cd)))
    return km


def inl_keyboard(next_calls: tuple[str] = None, back_opt: str = None) -> InlineKeyboardMarkup:
    """
    Функція створює інлайн-клавіатуру з кнопками, що базуються на next_calls,
    Та кнопкою '< Назад', якщо колбек містить можливість повернутися до
    'материнського' колбеку
    """
    options = dict()
    if next_calls is not None:
        options = {nxt_opt: callback_info[nxt_opt] for nxt_opt in next_calls}
    buttons = (InlineKeyboardButton(text=opt.btn_name,
                                    url=opt.url,
                                    callback_data=call)
               for call, opt in options.items())
    kb = InlineKeyboardMarkup(row_width=1).add(*buttons)
    if back_opt is not None:
        kb.add(InlineKeyboardButton(text='< Назад', callback_data='<' + back_opt))
    return kb


def get_info(call: str) -> (str, tuple[str], str):
    """
    Функція, що витягує з словника callback_info за ключем call
    повідомлення, яке треба вивести, колбеки наступних кнопок
    і інформацію про 'материнський' колбек (кнопки '< Назад')
    """
    info = callback_info[call]
    msg = info.msg
    next_calls = info.next_calls
    back_opt = info.back_opt
    return msg, next_calls, back_opt
