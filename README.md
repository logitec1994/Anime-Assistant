# Anime Assistant Bot

Telegram бот для управления списком аниме и манги.

## Возможности

- 📝 Добавление аниме и манги в список
- 📋 Просмотр всего списка
- 📊 Обновление статуса (просмотрено/хочу посмотреть)
- 🎯 Простой и удобный интерфейс

## Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd Anime-Assistant
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте файл `.env` в корне проекта:
```env
BOT_TOKEN=your_bot_token_here
DATABASE_URL=sqlite:///media.db
```

4. Получите токен бота у [@BotFather](https://t.me/BotFather) и добавьте его в `.env`

## Запуск

### Запуск бота:
```bash
python run_bot.py
```

### Тестирование основного функционала:
```bash
python main.py
```

## Команды бота

- `/start` - Приветствие и список команд
- `/help` - Подробная справка
- `/list` - Показать все аниме/мангу
- `/add` - Добавить новое аниме/мангу
- `/update <id> <status>` - Обновить статус

### Примеры использования:

```
/add
> Введите название: Naruto
> Выберите категорию: 1 (anime)

/update 1 watched
> Статус обновлен на "просмотрено"

/list
> Показать весь список
```

## Структура проекта

```
Anime-Assistant/
├── bot/                 # Telegram бот
│   ├── __init__.py
│   ├── bot.py          # Основной файл бота
│   └── handlers.py     # Обработчики команд
├── database/           # Работа с базой данных
├── models/             # Модели данных
├── repositories/       # Репозитории для работы с БД
├── services/           # Бизнес-логика
├── config.py          # Конфигурация
├── main.py            # Тестовый файл
├── run_bot.py         # Запуск бота
└── requirements.txt   # Зависимости
```

## Технологии

- Python 3.8+
- aiogram 3.x (Telegram Bot API)
- SQLAlchemy (ORM)
- SQLite (база данных)