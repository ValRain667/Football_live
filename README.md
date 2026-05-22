# Football Live Hub

Современная платформа для просмотра расписания футбольных матчей, турнирных таблиц, статистики команд и live-результатов.

## Архитектура

- **Frontend**: Nuxt 3 + Vue 3 + TypeScript + TailwindCSS + Pinia + Vue Query
- **Backend**: FastAPI + Python 3.12+ + PostgreSQL + SQLAlchemy + Redis + WebSocket

## Локальный запуск

### Требования

- Node.js 18+
- Python 3.12+
- PostgreSQL
- Redis

### Backend

```bash
cd backend

# Создайте виртуальное окружение (опционально)
python -m venv venv
venv\Scripts\activate  # Windows

# Установите зависимости
pip install -r requirements.txt

# Создайте файл .env на основе .env.example и настройте переменные
# DATABASE_URL=postgresql://postgres:password@localhost/football_live_hub
# JWT_SECRET=your_secret
# REDIS_URL=redis://localhost:6379
# FOOTBALL_API_KEY=YOUR_API_KEY

# Запустите сервер
uvicorn main:app --reload
```

API будет доступен по адресу: `http://localhost:8000`

### Frontend

```bash
cd frontend

# Установите зависимости
npm install

# Создайте файл .env на основе .env.example
# NUXT_PUBLIC_API_URL=http://localhost:8000

# Запустите dev-сервер
npm run dev
```

Frontend будет доступен по адресу: `http://localhost:3000`

## Структура проекта

```
├── backend/
│   ├── app/
│   │   ├── api/           # API роуты (matches, teams, leagues, standings, auth)
│   │   ├── auth/          # JWT, OAuth, bcrypt
│   │   ├── database.py    # SQLAlchemy engine и сессии
│   │   ├── models/        # Модели БД (User, FavoriteTeam, MatchCache)
│   │   ├── schemas/       # Pydantic схемы
│   │   ├── services/      # Бизнес-логика и кеширование (Redis)
│   │   └── websocket/     # WebSocket для live-обновлений
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── components/        # Vue компоненты
│   ├── composables/       # Composition API composables
│   ├── layouts/           # Nuxt layouts
│   ├── middleware/        # Route middleware
│   ├── pages/             # Nuxt pages (file-based routing)
│   ├── plugins/           # Nuxt plugins
│   ├── server/routes/     # Server routes (robots.txt, sitemap.xml)
│   ├── services/          # API клиенты
│   ├── stores/            # Pinia stores
│   ├── types/             # TypeScript типы
│   └── utils/             # Утилиты
└── README.md
```

## Основные функции

- **Live матчи** — реальное время с WebSocket обновлениями
- **Турнирные таблицы** — цветовое выделение зон ЛЧ и вылета
- **Команды и лиги** — детальная информация и статистика
- **Избранное** — сохранение любимых команд и матчей
- **Поиск** — глобальный поиск с debounce
- **Темная тема** — переключение dark/light
- **Авторизация** — JWT + OAuth (Google/GitHub)
- **SEO** — SSR, meta tags, sitemap, robots.txt

## API Endpoints

| Endpoint | Описание |
|----------|----------|
| `GET /api/matches` | Список матчей |
| `GET /api/matches/live` | Live матчи |
| `GET /api/matches/{id}` | Детали матча |
| `GET /api/teams` | Список команд |
| `GET /api/teams/{id}` | Детали команды |
| `GET /api/leagues` | Список лиг |
| `GET /api/leagues/{id}` | Детали лиги |
| `GET /api/standings/{leagueId}` | Турнирная таблица |
| `POST /api/auth/register` | Регистрация |
| `POST /api/auth/login` | Авторизация |
| `GET /api/auth/me` | Профиль пользователя |
| `WS /api/ws/live` | WebSocket live обновления |

## Безопасность

- Rate limiting
- Bcrypt хеширование паролей
- JWT access + refresh tokens
- CORS настроен для localhost:3000
- Pydantic валидация всех входных данных
