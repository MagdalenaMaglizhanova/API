FROM python:3.10-slim

# Инсталирай SWI-Prolog
RUN apt-get update && \
    apt-get install -y swi-prolog && \
    apt-get clean

# Копирай файловете
WORKDIR /app
COPY . /app

# Инсталирай Python зависимости
RUN pip install -r requirements.txt

# Стартирай Flask
CMD ["python", "app.py"]
