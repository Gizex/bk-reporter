import csv
import datetime
# Читаем исходный файл в память с заменой разделителя
data = []
with open('data-export.csv', 'r', encoding='utf-8') as csv_in:
    reader = csv.reader(csv_in, delimiter=',')
    for row in reader:
        data.append(row)  # Save row as list

# Фильтрация и переименование столбцов
required_cols = ['containerName', 'Name', 'Network Name', 'Number of CPUs', 'Memory MB', 'Total Storage Allocated MB', 'Status']
new_cols = ['Project', 'containerName', 'Name', 'Network Name', 'CPUs', 'Memory MB', 'Storage MB', 'Status']

filtered_data = []  # To store filtered data

headers = data[0]  # get the headers from first line
indices = [headers.index(col) for col in required_cols]  # get index of each required column in csv file

for row in data[1:]:
    new_row = [row[index] for index in indices]
    parts = new_row[1].split('-')
    if len(parts) >= 3:
        if parts[1] in ['stage', 'preprod', 'int']:
            parts[1] = 'dev'
        if parts[2] in ['qa', 'monitoring', 'test', 'template', 'ci', 'stpage', 'cmdb']:
            parts[2] = 'infra'
        if parts[2] in ['ml', 'superset', 'recsys']:
            parts[2] = 'analytics'
        if parts[2] in ['stoplist', 'userv', 'static', 'cadmin']:
            parts[2] = 'mpback'
        if parts[2] == 'ksk':
            parts[2] = 'kiosk'
        project = f"{parts[1].upper()}-{parts[2].upper()}"
    else:
        project = "UNKNOWN"
    if new_row[0] in ['QA', 'QA-NEW']:  # Исправлено условие на new_row[0]
        project = 'DEV-INFRA'  # Условие для значения 'QA' или 'QA-NEW'
    new_row.insert(0, project)
    filtered_data.append(new_row)


# Sort filtered data by 'Project'
filtered_data.sort(key=lambda x: x[0])



# Получаем текущую дату
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Получаем первое слово из столбца 'Name' для формирования названия файла
first_word = filtered_data[3][2].split('-')[0]

# Формируем имя файла с текущей датой и первым словом из столбца 'Name'
filename = f"{first_word} Отчет о потреблении ресурсов {current_date}.csv"

import pandas as pd

# Create dataframe from your filtered data
df = pd.DataFrame(filtered_data, columns=new_cols)

# Ensure the numeric columns are treated as such
df[['CPUs', 'Memory MB', 'Storage MB']] = df[['CPUs', 'Memory MB', 'Storage MB']].apply(pd.to_numeric)

# Create pivot table
pivot_df = df.pivot_table(index='Project', 
                          values=['CPUs', 'Memory MB', 'Storage MB'], 
                          aggfunc='sum')

# Save as an excel file with two sheets, one with original data and the second with the pivot table
with pd.ExcelWriter(f"{first_word} Отчет о потреблении ресурсов {current_date}.xlsx", engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Original Data', index=False)
    pivot_df.to_excel(writer, sheet_name='Pivot Table')

