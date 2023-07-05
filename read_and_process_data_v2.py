import logging
import csv

# Настройка логирования
logging.basicConfig(
    filename='app.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    datefmt='%d-%b-%y %H:%M:%S'
)
def read_and_process_data_v2(filename):
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
            
        if new_row[1] == 't1-prod-infra-usergate-1' or new_row[1] == 't1-prod-infra-usergate-2':
            project = 'PROD-INFRA'
        elif new_row[0] in ['KSK']:
            project = 'PROD-KIOSK'
        else:
            parts = new_row[0].split('-')
            if len(parts) >= 3:
                if parts[1] in ['ELK','QA','STPAGE']:
                    parts[1] = 'INFRA'
                if parts[1] in ['STOPLIST','USERV','STATIC','CADMIN']:
                    parts[1] = 'MPBACK'
                if parts[1] in ['ML', 'SUPERSET', 'RECSYS']:
                    parts[1] = 'ANALYTICS'
                if parts[1] in ['KSK']:
                    parts[1] = 'KIOSK'
                project = f"{parts[0].upper()}-{parts[1].upper()}"
            else:
                project = "UNKNOWN"


        new_row.insert(0, project)
        filtered_data.append(new_row)

    # Sort filtered data by 'Project'
    filtered_data.sort(key=lambda x: x[0])

    logging.info(f"Обработано {len(filtered_data)} строк")

    return filtered_data, new_cols
