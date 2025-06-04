FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

# -------------------------------
# Инструкция по запуску контейнера:
#
# 1. Сборка образа:
# docker build . --tag url_alias_app
#
# 2. Запуск контейнера:
# docker run -p 80:80 url_alias_app
#
# Или одной командой:
# docker build . --tag url_alias_app && docker run -p 80:80 url_alias_app
# -------------------------------
