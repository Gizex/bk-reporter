# Используем официальный образ Python для запуска Flask
FROM python:3.8-slim-buster

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Скопируем текущий каталог (где находится ваш Flask app) в рабочую директорию внутри контейнера
COPY . /app

# Устанавливаем необходимые пакеты
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Установим Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт 5000 для Flask
EXPOSE 5000

# Запускаем приложение
CMD ["python", "app.py"]
