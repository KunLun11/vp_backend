# Volley Pro

Волейбольная платформа: поиск, запись и организация игр.

## Быстрый старт

### 1. Backend

```bash
cd vp_backend

# Копировать .env
cp .env.example .env

# Установить зависимости (через uv)
uv sync

# Применить миграции
uv run python manage.py migrate

# Создать суперпользователя (для админки)
uv run python manage.py createsuperuser

# Запустить сервер (требуются Postgres + Redis)
uv run daphne -b 0.0.0.0 -p 8000 config.asgi:application
```

**Требования:**
- Python 3.13
- PostgreSQL (запущен, с БД `volley_pro`)
- Redis (запущен на 127.0.0.1:6379)
- Настроенный `.env` файл (особенно email для отправки кодов)

### 2. Frontend

```bash
cd vp_frontend

# Установить зависимости
npm install

# Запустить dev-сервер (на порту 3000, проксирует /api и /ws на 8000)
npm run dev
```

Фронтенд будет доступен по адресу: `http://localhost:3000`

**Vite proxy настроен** — запросы к `/api` и `/ws` автоматически проксируются на `127.0.0.1:8000`, CORS не требуется в dev-режиме.

## Структура Frontend

```
vp_frontend/
├── src/
│   ├── api/client.ts          # HTTP-клиент + все типы
│   ├── contexts/AuthContext   # Состояние авторизации
│   ├── components/
│   │   ├── Layout.tsx          # Обёртка с навбаром
│   │   ├── Navbar.tsx          # Навигация
│   │   └── ProtectedRoute.tsx  # Защита роутов
│   └── pages/
│       ├── Login.tsx           # Вход
│       ├── Register.tsx        # Регистрация
│       ├── VerifyEmail.tsx     # Подтверждение email
│       ├── Profile.tsx         # Профиль игрока
│       ├── Games.tsx           # Список игр
│       ├── GameDetail.tsx      # Детали игры + запись
│       └── Chat.tsx            # Чат игры (WebSocket)
```

## Страницы и функционал

| Страница | Путь | Описание |
|----------|------|----------|
| Вход | `/login` | Авторизация по email + пароль |
| Регистрация | `/register` | Создание аккаунта (player/organizer/coach) |
| Подтверждение email | `/verify-email?email=...` | Ввод 6-значного кода |
| Профиль | `/profile` | Просмотр/создание/редактирование профиля |
| Список игр | `/games` | Фильтр по статусу, карточки игр |
| Детали игры | `/games/:id` | Инфо, запись, действия организатора |
| Чат | `/games/:id/chat` | WebSocket-чат для участников игры |

## API

Документация: `http://localhost:8000/api/docs/swagger/`
