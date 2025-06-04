# URL Alias Service

Простой сервис сокращения ссылок на FastAPI.

## Возможности

- Регистрация и вход
- Сокращение ссылок с установкой срока действия
- Подсчёт переходов
- Деактивация ссылок
- Топ популярных ссылок
- Фоновая задача на очистку просроченных ссылок

---

### Локальный запуск (без Docker)

1. **Клонируй репозиторий**

```bash
git clone https://github.com/Luxsarba/URLAliasService.git
cd URLAliasService
````

2. **Создай виртуальное окружение и активируй его**

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

3. **Установи зависимости**

```bash
pip install -r requirements.txt
```

4. **Создай .env файл**
```
JWT_SECRET_KEY=JWT_SECRET_KEY
```

5. **Запусти сервер**

```bash
uvicorn app.main:app --reload
```

Теперь сервис доступен по ссылке: http://127.0.0.1:8000/docs

---

### Запуск с помощью Docker

1. **Создай .env файл**
```
JWT_SECRET_KEY=JWT_SECRET_KEY
```

2. **Построй образ**

```bash
docker build . --tag url_alias_app
```

3. **Запусти контейнер**

```bash
docker run -p 80:80 url_alias_app
```

Открой в браузере: http://localhost/docs
