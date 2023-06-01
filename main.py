import datetime
import pandas as pd
from read_and_process_data import read_and_process_data

# Чтение и обработка данных из CSV файла
data, new_cols = read_and_process_data('data-export.csv')

# Преобразование обработанных данных в DataFrame
df = pd.DataFrame(data, columns=new_cols)

# Убеждаемся, что числовые колонки обрабатываются как таковые
df[['CPUs', 'Memory MB', 'Storage MB']] = df[['CPUs', 'Memory MB', 'Storage MB']].apply(pd.to_numeric)

# Создание сводной таблицы
pivot_df = df.pivot_table(index='Project', 
                          values=['CPUs', 'Memory MB', 'Storage MB'], 
                          aggfunc='sum')

# Получение текущей даты
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Получение первого слова из столбца 'Name' для формирования названия файла
first_word = data[3][2].split('-')[0]

# Сохранение DataFrame и сводной таблицы в excel файл с двумя листами
with pd.ExcelWriter(f"{first_word} Отчет о потреблении ресурсов {current_date}.xlsx", engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Original Data', index=False)
    pivot_df.to_excel(writer, sheet_name='Pivot Table')
