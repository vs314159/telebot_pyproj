import pandas as pd


def remaining_lessons(name: str):
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
    df = pd.DataFrame({
        "Ім'я": [name],
        "Формат навчання": [study_format],
        "Кількість занять": [amount_of_lessons],
        "Сумма": [money]
    })
    df.to_csv('Students_all_data.csv', mode='a', index=False, header=False, encoding='utf-8-sig', sep=';')
