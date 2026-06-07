# Инструкция по подключению БД к сайту 33 Зуб

## 1. Создание базы данных

### Вариант A: Через консоль MySQL
```bash
mysql -u root -p
```

```sql
CREATE DATABASE 33teeth_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER '33teeth_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON 33teeth_db.* TO '33teeth_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Вариант B: Через phpMyAdmin
1. Войдите в phpMyAdmin
2. Создайте БД `33teeth_db` с кодировкой `utf8mb4_unicode_ci`
3. Перейдите во вкладку "Привилегии" и создайте пользователя

## 2. Импорт структуры

```bash
mysql -u root -p 33teeth_db < database/schema.sql
```

Или через phpMyAdmin:
- Выберите БД → Импорт → загрузите `database/schema.sql` → Выполнить

## 3. Настройка подключения

Отредактируйте файл `php/config/db.php`:

```php
// --- Настройки базы данных MySQL ---
define('DB_HOST', 'localhost');           // Хост MySQL
define('DB_NAME', '33teeth_db');          // Имя БД
define('DB_USER', '33teeth_user');        // Ваш пользователь
define('DB_PASS', 'secure_password');     // Ваш пароль
define('DB_CHARSET', 'utf8mb4');

// --- Настройки Yandex SMTP ---
define('SMTP_HOST', 'smtp.yandex.ru');
define('SMTP_PORT', 587);
define('SMTP_ENCRYPTION', 'tls');
define('SMTP_USER', 'zub.stomatolog.33@yandex.ru');  // Ваш Яндекс-адрес
define('SMTP_PASS', 'Пароль_приложения');           // Пароль приложения из Яндекс ID
define('SMTP_FROM_NAME', '33 Зуб');

// --- Секретный ключ для рассылки ---
define('NEWSLETTER_SECRET', 'ваш_секретный_ключ');
```

## 4. Получение пароля приложения Яндекса

1. Перейдите в [Яндекс ID](https://passport.yandex.ru/profile)
2. Раздел "Пароли и явки" → "Пароли приложений"
3. Создайте новый пароль приложения для SMTP
4. Скопируйте пароль в `vjxzorkhezeluywh`

## 5. Проверка подключения

Создайте файл `php/test-db.php`:

```php
<?php
require_once 'config/db.php';
try {
    $pdo = getDbConnection();
    echo "Подключение успешно!";
} catch (Exception $e) {
    echo "Ошибка: " . $e->getMessage();
}
```

Откройте в браузере: `http://ваш-сайт/33teeth/php/test-db.php`

## 6. API эндпоинты

| Метод | URL | Описание |
|-------|-----|----------|
| POST | `/php/api/subscriber.php` | Подписка на рассылку `{email: "..."}` |
| DELETE | `/php/api/subscriber.php` | Отписка `{email: "..."}` |
| GET | `/php/api/subscriber.php` | Список подписчиков (админ) |
| POST | `/php/api/contact-query.php` | Отправка вопроса с контакта |
| GET | `/php/api/contact-query.php` | Список вопросов (админ) |

## 7. Админ-панель

Откройте `admin/login.html`, затем `admin/subscribers.html` или `admin/contacts-queries.html` для просмотра записей.

//# Подробное руководство по проверке работоспособности БД в локальной среде XAMPP

## 1. Процесс тестирования взаимодействия

### 1.1 Тестовые сценарии записи данных

**Сценарий A: Подписка на рассылку**
1. Откройте сайт в браузере: `http://localhost/33teeth/` (главная), `http://localhost/33teeth/contact.html` или `http://localhost/33teeth/about.html`
2. Найдите форму подписки в футере (footer) — поле ввода email + кнопка "Подписаться"
3. Введите тестовый email: `test-user@33teeth.local` и нажмите "Подписаться"
4. Данные отправляются через POST на `/php/api/subscriber.php` → запись в таблицу `subscribers`

**Сценарий B: Отправка контактного сообщения**
1. Перейдите на страницу: `http://localhost/33teeth/contact.html`
2. Заполните форму контактов:
   - Имя: `Тест Пользователь`
   - Email: `test-contact@33teeth.local`
   - Телефон: `+7 (999) 123-45-67`
   - Сообщение: `Тестовое сообщение для проверки БД`
3. Нажмите "Отправить" — POST запрос на `/php/api/contact-query.php` → запись в таблицу `feedback_messages`

**Сценарий C: Тестирование через cURL (для разработчиков)**
```bash
# Тест подписки
curl -X POST http://localhost/33teeth/php/api/subscriber.php ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"curl-test@33teeth.local\"}"

# Тест контактного сообщения
curl -X POST http://localhost/33teeth/php/api/contact-query.php ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"cURL Test\",\"email\":\"curl-contact@33teeth.local\",\"message\":\"Test via API\"}"
```

## 2. Верификация данных

### 2.1 Проверка в phpMyAdmin

1. Откройте phpMyAdmin: `http://localhost/phpmyadmin/`
2. Выберите базу данных `33teeth_db`
3. Откройте таблицу `subscribers` → вкладка "Просмотр" — найдите запись с email `test-user@33teeth.local`
4. Откройте таблицу `feedback_messages` — найдите запись с именем `Тест Пользователь`
5. Обновите страницу (F5) и убедитесь, что записи появились мгновенно

### 2.2 Проверка в административной панели

**Для подписчиков:**
1. Откройте `http://localhost/33teeth/admin/login.html`
2. Авторизуйтесь (проверьте логин/пароль в системе)
3. Перейдите в `admin/subscribers.html` — нажмите "Обновить"
4. Таблица отобразит новых подписчиков с указанием:
   - ID, Email, Статус (Активен/Отписан), Дата подписки

**Для контактных сообщений:**
1. Откройте `admin/contacts-queries.html` — нажмите "Обновить"
2. Таблица покажет новые записи с колонками: ID, Имя, Email, Телефон, Статус, Дата

### 2.3 Совместная верификация

| Этап | phpMyAdmin | Админ-панель | Ожидаемый результат |
|------|------------|---------------|---------------------|
| 1 | Запись появилась в таблице | Данные отображаются после "Обновить" | Совпадают |
| 2 | Статус `is_active = 1` | Статус "Активен" | Синхронизированы |
| 3 | Время создания совпадает | Дата в колонке совпадает | Временная метка корректна |

## 3. Проверка соединения и целостности

### 3.1 Проверка соединения PHP-PDO с MySQL

**Файл `php/test-db.php`:**
```php
<?php
require_once __DIR__ . '/config/db.php';
try {
    $pdo = getDbConnection();
    
    // Тест 1: Проверка соединения
    echo "✓ Соединение установлено\n";
    
    // Тест 2: Выполнение запроса
    $stmt = $pdo->query("SELECT COUNT(*) FROM subscribers");
    $count = $stmt->fetchColumn();
    echo "✓ Таблица subscribers: $count записей\n";
    
    // Тест 3: Проверка charset
    $stmt = $pdo->query("SHOW VARIABLES LIKE 'character_set_connection'");
    $charset = $stmt->fetch();
    echo "✓ Charset соединения: " . $charset['Value'] . "\n";
    
} catch (Exception $e) {
    echo "✗ Ошибка: " . $e->getMessage();
}
?>
```

**Запуск теста:** `http://localhost/33teeth/php/test-db.php`

### 3.2 Тестирование целостности данных (Data Integrity)

**Проверка через SQL-запросы в phpMyAdmin:**

```sql
-- Тест 1: Проверка уникальности email в подписчиках
SELECT email, COUNT(*) as cnt FROM subscribers GROUP BY email HAVING cnt > 1;

-- Тест 2: Проверка ссылочной целостности (внешние ключи)
SELECT * FROM newsletter_log 
WHERE subscriber_id NOT IN (SELECT id FROM subscribers);

-- Тест 3: Проверка не-null ограничений
SELECT * FROM feedback_messages WHERE name IS NULL OR email IS NULL OR message IS NULL;

-- Тест 4: Проверка ENUM-ограничений статуса
SELECT DISTINCT status FROM feedback_messages 
WHERE status NOT IN ('new', 'in_progress', 'completed');

-- Тест 5: Проверка временных меток
SELECT * FROM subscribers WHERE subscribed_at > NOW();
```

### 3.3 Автоматический тест целостности

**Создайте файл `php/test-integrity.php`:**
```php
<?php
require_once __DIR__ . '/config/db.php';
$pdo = getDbConnection();

$tests = [
    'unique_emails' => "SELECT COUNT(*) FROM (SELECT email FROM subscribers GROUP BY email HAVING COUNT(*) > 1) t",
    'orphan_logs' => "SELECT COUNT(*) FROM newsletter_log WHERE subscriber_id NOT IN (SELECT id FROM subscribers)",
    'null_names' => "SELECT COUNT(*) FROM feedback_messages WHERE name IS NULL OR email IS NULL",
    'invalid_status' => "SELECT COUNT(*) FROM feedback_messages WHERE status NOT IN ('new', 'in_progress', 'completed')",
];

foreach ($tests as $name => $sql) {
    $count = $pdo->query($sql)->fetchColumn();
    echo "$name: " . ($count == 0 ? "✓ OK" : "✗ FAIL ($count)") . "\n";
}
?>
```

### 3.4 Мониторинг соединения в реальном времени

**Проверка через консоль MySQL:**
```sql
-- Подключение к MySQL
mysql -u admin -p33teeth_db

-- Список активных соединений
SHOW PROCESSLIST;

-- Проверка последних запросов (если включён log)
SHOW ENGINE INNODB STATUS;
```

---

**Ключевые файлы системы:**
- `php/config/db.php` — конфигурация PDO соединения
- `php/api/subscriber.php` — API подписки (таблица `subscribers`)
- `php/api/contact-query.php` — API контактов (таблица `feedback_messages`)
- `database/schema.sql` — схема БД с внешними ключами
- `admin/subscribers.html` — админ-панель подписчиков
- `admin/contacts-queries.html` — админ-панель контактов