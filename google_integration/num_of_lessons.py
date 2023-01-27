import gspread
import pandas as pd
from setting import google_table_id

def get_data():
    gs = gspread.service_account(filename='google_integration/credits.json')  # подключаємо файл з ключами і тд.
    sh = gs.open_by_key(google_table_id)  # подключаємо таблицю по ID
    worksheet = sh.sheet1  # отримуємо перший лист
    return pd.DataFrame(data=worksheet.get_all_records())


def number_of_lessons_from_sheets(phone_number, df, number_col, balance_col):
    phone_number = int(phone_number)
    row = df[df[number_col] == phone_number]
    if len(row):
        balance_val = row[balance_col].values
        if balance_val < 0:
            return f'У Вас {balance_val} неоплачених занять. Внесіть, будь ласка, оплату'
        else:
            return f'У Вас залишилось {balance_val} оплачених занять. Хочете оплатити наперед?'


google_table_df = get_data()
