import gspread


async def number_of_lessons_from_sheets(message: types.Message):
    gs = gspread.service_account(filename='credits.json')  # подключаємо файл з ключами і тд.
    sh = gs.open_by_key('1p9KvkfjsJOs-7EfVVlysiMVCy6JWBsLXeJTdXsoPbVs')  # подключаємо таблицю по ID
    worksheet = sh.sheet1  # отримуємо перший лист

    res = worksheet.get_all_records()  # виклик всіх даних з таблиці

    name = input("Enter your name: ")  # цей рядок для перевірки | його треба прибрати | і замінити на номер
    num = 0  # для циклу з пошуку потрібного учня

    for lessons in res:
        if res[num]['Ученик'] == name.title():
            # перевірка зараз за ім'ям відбувається, "name" замінюємо на змінну, що відповідає за номер
            num_lessons = res[num]['баланс уроков']  # тут викликається з таблички колонка, що містить залишок уроків
            if int(num_lessons) <= 0:
                await message.answer(f"Кількість сплачених занять: {res[num]['баланс уроков']}")
                await message.answer(
                    f"Упс! 🤭\nЗалишок занять менше 1 \nрекомендуємо поповнити баланс 👇🏼")
                # тут треба додати кнопку на функцію з поповнення кількості занять
            else:
                await message.answer(f"Кількість сплачених занять: {res[num]['баланс уроков']} ")
                await message.answer(f"До зустрічі на заняттях! 😉")
                # тут треба додати кнопки головного меню, чи куди воно має повертатись
        num += 1