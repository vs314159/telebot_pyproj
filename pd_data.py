import pandas as pd


def remaining_lessons(name: str):
    """Повертає кількість занять за іменем студента. Якщо його немає в базі - повертає NOne"""
    name = ' '.join(word.capitalize() for word in name.split())
    df = pd.read_csv('Students_lessons.csv', sep=';')

    name_ind = df.index[df["Ім'я"] == name].tolist()
    rem_lessons = df["Кількість занять"].values[name_ind]
    if rem_lessons.size > 0:
        return rem_lessons[0]


def write_to_cvs(name: str, study_format: str, amount_of_lessons: str, money: str) -> None:
    """Записує дані в файл 'Students_all_data.csv'"""
    name = ' '.join(word.capitalize() for word in name.split())
    df = pd.DataFrame({
        "Ім'я": [name],
        "Формат навчання": [study_format],
        "Кількість занять": [amount_of_lessons],
        "Сумма": [money]
    })
    df.to_csv('Students_all_data.csv', mode='a', index=False, header=False, encoding='utf-8-sig', sep=';')


def is_student(name: str) -> bool:
    """Перевірка наявності студента у базі данних"""
    name = ' '.join(word.capitalize() for word in name.split())
    df = pd.read_csv('Students_lessons.csv', sep=';')
    return (df["Ім'я"] == name).any()
