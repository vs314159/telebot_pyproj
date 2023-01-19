import pandas as pd


def remaining_lessons(name: str):
<<<<<<< HEAD
    """Повертає кулькість занять за іменем студента. Якщо його немає в базі - повертає NOne"""
    name = ' '.join(word.capitalize() for word in name.split())
    df = pd.read_csv('Students_lessons.csv', sep=';')

    name_ind = df.index[df["Ім'я"] == name].tolist()
    rem_lessons = df["Кількість занять"].values[name_ind]
    if rem_lessons.size > 0:
        return rem_lessons[0]


def write_to_cvs(name: str, study_format: str, amount_of_lessons: str, money: str) -> None:
    """Записує дані в файл 'Students_all_data.csv'"""
    name = ' '.join(word.capitalize() for word in name.split())
=======
    """
    Повертає кулькість занять за іменем студента
    """
    df = pd.read_csv('Students_lessons.csv', sep=';')

    name_ind = df.index[df["Ім'я"] == name].tolist()
    ream_lessons = df["Кількість занять"].values[name_ind]
    if ream_lessons.size > 0:
        return ream_lessons[0]
    else:
        return None


def write_to_cvs(name: str, study_format: str, amount_of_lessons: str, money: str) -> None:
    """
    Записує дані в файл 'Students_all_data.csv'
    """
>>>>>>> 8d8ed83e2dacf299fc425e837015038f89cb16d1
    df = pd.DataFrame({
        "Ім'я": [name],
        "Формат навчання": [study_format],
        "Кількість занять": [amount_of_lessons],
        "Сумма": [money]
    })
    df.to_csv('Students_all_data.csv', mode='a', index=False, header=False, encoding='utf-8-sig', sep=';')
<<<<<<< HEAD


def is_student(name: str) -> bool:
    """Перевірка наявності студента у базі данних"""
    name = ' '.join(word.capitalize() for word in name.split())
    df = pd.read_csv('Students_lessons.csv', sep=';')
    return (df["Ім'я"] == name).any()
=======
>>>>>>> 8d8ed83e2dacf299fc425e837015038f89cb16d1
