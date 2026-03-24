FROM python:3.10-slim

# Рабочая директория внутри контейнера
WORKDIR /app

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