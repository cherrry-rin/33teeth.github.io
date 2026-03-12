# Настройка и запуск проекта "33 Зуб"

## Обзор проекта

Проект "33 Зуб" - это комплексное решение для стоматологической клиники, включающее:

1. **Backend** - FastAPI сервер с PostgreSQL базой данных
2. **Frontend** - Vue.js клиент для клиентов клиники
3. **Admin** - Vue.js админка для управления данными
4. **Интеграция** - HTML виджеты для существующего сайта

## Требования

- Python 3.9+
- Node.js 16+
- PostgreSQL 12+
- pip

## Установка и настройка

### 1. Установка Python зависимостей

```bash
cd backend
pip install -r requirements.txt
```

### 2. Настройка базы данных

1. Создайте базу данных в PostgreSQL:
```sql
CREATE DATABASE dental_clinic;
CREATE USER dental_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE dental_clinic TO dental_user;
```

2. Настройте `.env` файл в папке `backend/`:
```
DATABASE_URL=postgresql://dental_user:your_password@localhost:5432/dental_clinic
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Запуск backend сервера

```bash
cd backend
python main.py
```

Сервер будет доступен по адресу: `http://localhost:8000`

### 4. Установка frontend зависимостей

```bash
cd frontend
npm install
```

### 5. Запуск frontend клиентского приложения

```bash
cd frontend
npm run dev
```

Клиент будет доступен по адресу: `http://localhost:5173`

### 6. Установка admin зависимостей

```bash
cd admin
npm install
```

### 7. Запуск админки

```bash
cd admin
npm run dev
```

Админка будет доступна по адресу: `http://localhost:3001`

## Использование

### Клиентская часть (frontend)
- Главная страница с услугами и формой обратной связи
- Страница контактов с формой сообщения
- Автоматическая интеграция с backend API

### Админка
- Панель управления с обзором статистики
- Управление сообщениями (просмотр, изменение статуса)
- Управление услугами (в будущем)
- Управление подписчиками (в будущем)

### Интеграция с существующим сайтом
Используйте готовые HTML виджеты:
- `feedback-form.html` - форма обратной связи
- `newsletter-form.html` - форма подписки на рассылку

Просто вставьте эти файлы в ваш существующий HTML сайт.

## API endpoints

### Feedback (Обратная связь)
- `POST /api/v1/feedback/` - Создать сообщение
- `GET /api/v1/feedback/` - Получить все сообщения
- `GET /api/v1/feedback/{id}` - Получить сообщение по ID
- `PUT /api/v1/feedback/{id}` - Обновить сообщение
- `DELETE /api/v1/feedback/{id}` - Удалить сообщение

### Subscriber (Подписчики)
- `POST /api/v1/subscriber/` - Подписаться
- `GET /api/v1/subscriber/{email}` - Проверить подписку
- `DELETE /api/v1/subscriber/{email}` - Отписаться

## Безопасность

- JWT аутентификация для админки
- Валидация всех входящих данных
- Защита от SQL инъекций (используется SQLAlchemy)
- CORS настройки для безопасности

## Тестирование

Backend API можно тестировать через Swagger UI:
- Откройте `http://localhost:8000/docs`
- Там вы найдете интерактивную документацию API

## Возможные проблемы

### Port already in use
Если порт занят, измените порт в:
- `backend/main.py` - для backend сервера
- `frontend/vite.config.js` - для frontend
- `admin/vite.config.js` - для админки

### Database connection error
Проверьте:
- Запущен ли PostgreSQL сервер
- Правильность настроек в `.env` файле
- Доступ к базе данных

### CORS errors
Проверьте настройки CORS в `backend/main.py`

## Дальнейшее развитие

1. **Добавление аутентификации для клиентов**
2. **Расписание приемов и онлайн-запись**
3. **CRM система для управления пациентами**
4. **Email рассылки и уведомления**
5. **Мобильное приложение**
6. **Интеграция с платежными системами**

## Поддержка

Для вопросов и поддержки:
- Проверьте логи backend сервера
- Используйте Swagger UI для тестирования API
- Проверьте консоль браузера на наличие ошибок frontend