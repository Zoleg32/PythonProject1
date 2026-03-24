FROM python:3.10-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Устанавливаем системные зависимости (если нужны)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/* \

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Открываем порт Flask
EXPOSE 5000

# Команда запуска
CMD ["python", "main.py"]