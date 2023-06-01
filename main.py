import csv

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

for row in data[1:]:  # skip header row
    new_row = [row[index] for index in indices]  # select only required columns for each row
    # Generate 'Project' field value
    parts = new_row[1].split('-')
    if len(parts) >= 3:
        if parts[1] in ['stage', 'preprod','int']:
            parts[1] = 'dev'
        if parts[2] in ['qa', 'monitoring', 'test', 'template', 'ci','stpage']:
            parts[2] = 'infra'
        if parts[2] in ['ml', 'superset', 'recsys']:
            parts[2] = 'analytics'
        if parts[2] in ['stoplist', 'userv','static']:
            parts[2] = 'mpback'
        if parts[2] == 'ksk':
            parts[2] = 'kiosk'
        project = f"{parts[1].upper()}-{parts[2].upper()}"
    else:
        project = "UNKNOWN"
    # Add 'Project' to the beginning of the row
    new_row.insert(0, project)
    filtered_data.append(new_row)

# Sort filtered data by 'Project'
filtered_data.sort(key=lambda x: x[0])

# Write filtered data to new file
with open('data-export-filtered.csv', 'w', newline='', encoding='utf-8') as csv_out:
    writer = csv.writer(csv_out, delimiter=';')
    writer.writerow(new_cols)  # write new headers
    writer.writerows(filtered_data)  # write filtered data
