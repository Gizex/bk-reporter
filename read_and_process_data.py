import logging
import csv

# Настройка логирования
logging.basicConfig(filename='app.log', level=logging.INFO)

def read_and_process_data(filename):
    """ 
    Функция для чтения и обработки CSV файла.
    Возвращает обработанные данные и новые заголовки колонок.
    """
    # Чтение исходного файла в память с заменой разделителя
    data = []
    with open(filename, 'r', encoding='utf-8') as csv_in:
        reader = csv.reader(csv_in, delimiter=',')
        for row in reader:
            data.append(row)  # Save row as list

    logging.info(f"Прочитано {len(data)} строк из файла: {filename}")

    # Фильтрация и переименование столбцов
    required_cols = ['containerName', 'Name', 'Network Name', 'Number of CPUs', 'Memory MB', 'Total Storage Allocated MB', 'Status']
    new_cols = ['Project', 'containerName', 'Name', 'Network Name', 'CPUs', 'Memory GB', 'Storage GB', 'Status']
    filtered_data = []  # To store filtered data

    headers = data[0]  # get the headers from first line
    indices = [headers.index(col) for col in required_cols]  # get index of each required column in csv file

    for row in data[1:]:
        new_row = [row[index] for index in indices]
        
        memory_index = required_cols.index('Memory MB')
        storage_index = required_cols.index('Total Storage Allocated MB')
        
        # Проверка на наличие данных в столбцах перед преобразованием
        if new_row[memory_index]:
            new_row[memory_index] = float(new_row[memory_index]) / 1024
        if new_row[storage_index]:
            new_row[storage_index] = float(new_row[storage_index]) / 1024
            
        parts = new_row[1].split('-')
        if len(parts) >= 3:
            if parts[1] in ['stage', 'preprod', 'int']:
                parts[1] = 'dev'
            if parts[1] in ['qa'] and parts[2] in ['mpback']:
                parts[1] = 'prod' 
                parts[2] = 'infra'
            if parts[2] in ['qa', 'monitoring', 'test', 'template', 'ci', 'stpage', 'cmdb']:
                parts[2] = 'infra'
            if parts[2] in ['ml', 'superset', 'recsys']:
                parts[2] = 'analytics'
            if parts[2] in ['stoplist', 'userv', 'static', 'cadmin']:
                parts[2] = 'mpback'
            if parts[2] in ['ksk','fariton']:
                parts[2] = 'kiosk'
            project = f"{parts[1].upper()}-{parts[2].upper()}"
        else:
            project = "UNKNOWN"
        
        # Проверка условия для DEV-DEVSECOPS или PROD-DEVSECOPS
        if 'DEVSECOPS' in new_row[0]:
            if 'dev' in parts[1].lower():
                project = 'DEV-DEVSECOPS'
            elif 'prod' in parts[1].lower():
                project = 'PROD-DEVSECOPS'

        new_row.insert(0, project)
        filtered_data.append(new_row)

    # Sort filtered data by 'Project'
    filtered_data.sort(key=lambda x: x[0])

    logging.info(f"Обработано {len(filtered_data)} строк")

    return filtered_data, new_cols
