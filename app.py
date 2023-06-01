from flask import Flask, request, render_template, send_file
import datetime
import pandas as pd
from read_and_process_data import read_and_process_data
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Получение загруженного файла
        file = request.files['file']

        # Проверка и создание папки 'uploads', если она не существует
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        # Сохранение загруженного файла на сервере
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Чтение и обработка данных из загруженного CSV файла
        data, new_cols = read_and_process_data(file_path)

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
        result_file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{first_word} Отчет о потреблении ресурсов {current_date}.xlsx")
        with pd.ExcelWriter(result_file_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Original Data', index=False)
            pivot_df.to_excel(writer, sheet_name='Pivot Table')

        # Удаление загруженного файла после обработки
        os.remove(file_path)

        # Отправка файла для скачивания
        return send_file(result_file_path, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')