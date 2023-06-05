# Используем официальный образ Python для запуска Flask
FROM python:3.11-slim-buster

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем только файл requirements.txt вначале для лучшего использования кеша Docker
COPY ./requirements.txt .

# Установим Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем текущий каталог (где находится ваш Flask app) в рабочую директорию внутри контейнера
COPY . /app

# Открываем порт 5000 для Flask
EXPOSE 5000

# Запускаем приложение через gunicorn для продакшен среды
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
