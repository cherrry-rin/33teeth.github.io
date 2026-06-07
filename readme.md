# 🦷 33 Зуб - Стоматологическая клиника

Комплексное решение для автоматизации стоматологической клиники "33 Зуб". Проект включает в себя backend API, клиентский frontend, админку и готовые HTML виджеты для интеграции с существующим сайтом.

## 🎯 Возможности

### Для клиентов
- 📋 Просмотр услуг и цен
- 📝 Онлайн-запись и оставление отзывов
- 📧 Подписка на рассылку новостей
- 📞 Контактная форма

### Для администраторов
- 📊 Панель управления с обзором статистики
- 📨 Управление сообщениями (просмотр, изменение статуса)
- 👥 Управление подписчиками
- 🔧 Настройка услуг и цен

### Для интеграции
- 📄 Готовые HTML виджеты для существующего сайта
- 🔌 REST API для интеграции с другими системами
- 🛡️ Безопасная аутентификация и валидация

## 🏗️ Архитектура

```
33 Зуб
├── Backend (FastAPI + PostgreSQL)
│   ├── API для обратной связи
│   ├── API для подписчиков
│   ├── Аутентификация JWT
│   └── ORM SQLAlchemy
├── Frontend (Vue.js)
│   ├── Главная страница с услугами
│   ├── Страница контактов
│   ├── Формы обратной связи
│   └── Интеграция с backend
├── Admin (Vue.js)
│   ├── Панель управления
│   ├── Управление сообщениями
│   ├── Статистика
│   └── Управление данными
└── Integration
    ├── feedback-form.html
    ├── newsletter-form.html
    └── Готовые виджеты
```

## 🚀 Быстрый старт

### Требования
- Python 3.9+
- Node.js 16+
- PostgreSQL 12+

### 1. Автоматическая установка
```bash
# Запустите скрипт для автоматической настройки
start-all.bat
```

### 2. Ручная установка

#### Backend
```bash
cd backend
pip install -r requirements.txt
# Настройте .env файл
python main.py
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

#### Admin
```bash
cd admin
npm install
npm run dev
```

### 3. Тестирование
```bash
python test-setup.py
```

## 📋 Сервисы

После запуска все сервисы будут доступны:

- **Backend API**: http://localhost:8000
- **Frontend**: http://localhost:5173
- **Admin Panel**: http://localhost:3001

### API Endpoints

#### Обратная связь
- `POST /api/v1/feedback/` - Создать сообщение
- `GET /api/v1/feedback/` - Получить все сообщения
- `GET /api/v1/feedback/{id}` - Получить сообщение по ID
- `PUT /api/v1/feedback/{id}` - Обновить сообщение
- `DELETE /api/v1/feedback/{id}` - Удалить сообщение

#### Подписчики
- `POST /api/v1/subscriber/` - Подписаться
- `GET /api/v1/subscriber/{email}` - Проверить подписку
- `DELETE /api/v1/subscriber/{email}` - Отписаться

## 🔧 Конфигурация

### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/dental_clinic
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (vite.config.js)
```javascript
server: {
  port: 5173,
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    }
  }
}
```

### Admin (vite.config.js)
```javascript
server: {
  port: 3001,
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    }
  }
}
```

## 📊 База данных

Проект использует PostgreSQL с следующими таблицами:

- `feedback` - Сообщения от клиентов
- `subscribers` - Подписчики на рассылку
- `users` - Пользователи системы (в будущем)
- `services` - Услуги клиники (в будущем)

## 🛡️ Безопасность

- JWT аутентификация для админки
- Валидация всех входящих данных
- Защита от SQL инъекций (SQLAlchemy)
- CORS настройки
- Хранение паролей с хешированием

## 📱 Интеграция с существующим сайтом

### Форма обратной связи
Вставьте содержимое `feedback-form.html` в ваш сайт:

```html
<!-- Вставьте этот код в ваш HTML файл -->
<div id="feedback-widget"></div>
<script src="feedback-form.html"></script>
```

### Форма подписки
Вставьте содержимое `newsletter-form.html` в ваш сайт:

```html
<!-- Вставьте этот код в ваш HTML файл -->
<div id="newsletter-widget"></div>
<script src="newsletter-form.html"></script>
```

## 🧪 Тестирование

### Автоматическое тестирование
```bash
python test-setup.py
```

### Ручное тестирование
1. Откройте Swagger UI: http://localhost:8000/docs
2. Протестируйте API endpoints
3. Проверьте frontend: http://localhost:5173
4. Проверьте админку: http://localhost:3001

## 🚨 Возможные проблемы

### Port already in use
Измените порты в конфигурационных файлах:
- Backend: `main.py`
- Frontend: `vite.config.js`
- Admin: `vite.config.js`

### Database connection error
Проверьте:
- Запущен ли PostgreSQL
- Правильность настроек в `.env`
- Доступ к базе данных

### CORS errors
Проверьте настройки CORS в `backend/main.py`

## 🔄 Дальнейшее развитие

### Планы по улучшению
1. **Онлайн-запись на прием**
2. **CRM система для пациентов**
3. **Email рассылки и уведомления**
4. **Мобильное приложение**
5. **Интеграция с платежными системами**
6. **Статистика и аналитика**

### Возможные интеграции
- Системы электронной очереди
- Платежные системы (Сбербанк, Тинькофф)
- Email сервисы (SendGrid, Mailchimp)
- SMS сервисы (SMS.ru, Twilio)
- CRM системы

## 📞 Поддержка

Для вопросов и поддержки:
1. Проверьте логи backend сервера
2. Используйте Swagger UI для тестирования API
3. Проверьте консоль браузера на наличие ошибок
4. Запустите `python test-setup.py` для диагностики

## 📄 Лицензия

Этот проект разработан для стоматологической клиники "33 Зуб". Все права защищены.

---

**33 Зуб** - Считаем зубы, дарим улыбки! 😊