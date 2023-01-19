import pandas as pd


def is_student(name: str) -> bool:
    """Перевірка наявності студента у базі данних"""
    name = ' '.join(word.capitalize() for word in name.split())
    df = pd.read_csv('Students_lessons.csv', sep=';')
    return (df["Ім'я"] == name).any()


def remaining_lessons(name: str):
    """Повертає кількість занять за іменем студента. Якщо його немає в базі - повертає NOne"""
    name = ' '.join(word.capitalize() for word in name.split())
    df = pd.read_csv('Students_lessons.csv', sep=';')

    name_ind = df.index[df["Ім'я"] == name].tolist()
    rem_lessons = df["Кількість занять"].values[name_ind]
    if rem_lessons.size > 0:
        return rem_lessons[0]


def write_student_data(name: str, study_format: str, amount_of_lessons: str, money: str) -> None:
    """Записує дані студента в файл 'Students_all_data.csv'"""
    name = ' '.join(word.capitalize() for word in name.split())
    df = pd.DataFrame({
        "Ім'я": [name],
        "Формат навчання": [study_format],
        "Кількість занять": [amount_of_lessons],
        "Сумма": [money]
    })
    df.to_csv('Students_all_data.csv', mode='a', index=False, header=False, encoding='utf-8-sig', sep=';')


def apply_for_trial_lesson(name: str, study_format: str, phone_number: str, suitable_time: str, test_res: str) -> None:
    """Записує дані студента, бажаючого потрапити на пробне заняття в файл 'Trial_lessons.csv'"""
    name = ' '.join(word.capitalize() for word in name.split())
    df = pd.DataFrame({
        "Ім'я": [name],
        "Формат навчання": [study_format],
        "Номер Телефону": [phone_number],
        "Зручний час": [suitable_time],
        "Результат тестування": [test_res]
    })
    df.to_csv('Trial_lessons.csv', mode='a', index=False, header=False, encoding='utf-8-sig', sep=';')


apply_for_trial_lesson(name='Анатолій Боднаренко',
                       study_format='індивідуально',
                       phone_number='987654321?',
                       suitable_time='Будь який час на вихідних',
                       test_res='B2')