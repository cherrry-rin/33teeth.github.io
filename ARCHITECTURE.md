# Архитектура взаимодействия Admin Panel ↔ Frontend

## 1. Общая архитектура

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│   Admin Panel    │     │   API Layer      │     │   Frontend       │
│  (vHd5Gz7qKl/)  │────►│  (/php/api/v2/)  │◄───│   (site.com)     │
│                  │     │                  │     │                  │
└────────┬─────────┘     └────────┬─────────┘     └────────┬─────────┘
         │                        │                        │
         │ Session/Token          │ PDO                      │ HTTP API
         ▼                        ▼                        ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      MySQL Database                                  │
│  ┌────────────┐ ┌─────────┐ ┌───────────────┐ ┌─────────────┐      │
│  │ services   │ │ users   │ │ admin_audit   │ │ subscribers │      │
│  └────────────┘ └─────────┘ └───────────────┘ └─────────────┘      │
└─────────────────────────────────────────────────────────────────────┘
```

## 2. Аутентификация администратора

### 2.1 Двухуровневая (рекомендуется)

**Session-based** (для админки):
- `$_SESSION['admin_logged_in']` + `$_SESSION['admin_id']`
- Используется в `header.php` для проверки

**Token-based** (для API):
- Bearer токен в заголовке `Authorization`
- Хранится в `users.token` с `token_expires`
- Срок: 24 часа (настраивается в `.env`)

### 2.2 JWT (альтернатива)

```php
// Генерация токена
$payload = [
    'sub' => $userId,
    'exp' => time() + 86400,
    'role' => 'admin'
];
$token = base64_encode(json_encode($payload)) . '.' . hash_hmac('sha256', $payload, $secret);
```

## 3. Безопасность передачи данных

### 3.1 HTTPS
```apache
# .htaccess
RewriteEngine On
RewriteCond %{HTTPS} !=on
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
```

### 3.2 CORS Whitelist
```php
// Разрешённые домены в .env
ALLOWED_ORIGINS=https://33zub.ru,https://www.33zub.ru

// Проверка в CorsMiddleware.php
if (!AppConfig::getInstance()->isCorsAllowed($origin)) {
    http_response_code(403);
    exit;
}
```

### 3.3 Rate Limiting
```php
// 100 запросов в минуту на IP
SecurityMiddleware::rateLimit(100, 60);
```

### 3.4 CSRF защита
```php
// Для форм
$_SESSION['csrf_token'] = bin2hex(random_bytes(32));
// Проверка: hash_equals($_SESSION['csrf_token'], $_POST['csrf'])
```

## 4. Синхронизация данных

### 4.1 Write-through кеш
При изменении через Admin API:
1. Обновление в БД
2. Инвалидация кеша (`invalidateServiceCache()`)
3. Frontend получает свежие данные при следующем запросе

### 4.2 ETag для оптимизации
```php
// Генерация ETag
$etag = md5(serialize($services) . $lastModified);
header('ETag: "' . $etag . '"');

// Проверка If-None-Match
if ($_SERVER['HTTP_IF_NONE_MATCH'] ?? '' === $etag) {
    http_response_code(304);
    exit;
}
```

### 4.3 Polling с фронтенда
```javascript
// Обновление каждые 30 секунд
setInterval(async () => {
    const resp = await fetch('/php/api/public/services.php', {
        headers: { 'If-None-Match': localStorage.getItem('services_etag') }
    });
    if (resp.status === 304) return; // Данные не изменились
    const services = await resp.json();
    updateUI(services);
}, 30000);
```

## 5. Realtime через SSE

### 5.1 Сервер
```php
// /php/api/events.php
header('Content-Type: text/event-stream');
header('Cache-Control: no-cache');

// Отправка события при изменении
echo "event: service.updated\ndata: {\"ts\":".time().."}\n\n";
```

### 5.2 Клиент
```javascript
const es = new EventSource('/php/api/events.php');
es.addEventListener('service.updated', () => loadServices());
```

## 6. Слои абстракции

```
Frontend (JS)
    │
    ▼
API Endpoints (v2/services.php)
    │
    ▼
Service Layer (ServiceService.php)
    │
    ▼
Repository Layer (ServiceRepository.php)
    │
    ▼
PDO/MySQL
```

## 7. Audit Trail

```sql
CREATE TABLE admin_audit_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(50), -- create/update/delete
    table_name VARCHAR(50), -- services
    record_id INT,
    old_values JSON,
    new_values JSON,
    ip_address VARCHAR(45),
    created_at TIMESTAMP
);
```

## 8. Деплой и миграции

```bash
# Миграция новых полей
mysql -u admin -p < php/sql/migration_services.sql

# Миграция аудит лога  
mysql -u admin -p < php/sql/migration_audit_log.sql
```

## 9. Мониторинг

### 9.1 Health check
```
GET /php/api/health.php
{
    "success": true,
    "checks": {
        "database": "ok",
        "storage_writable": "ok",
        "cache_writable": "ok"
    }
}
```

### 9.2 Логи
```bash
# Ошибки
tail -f /var/log/apache2/error.log

# Audit trail
SELECT * FROM admin_audit_log ORDER BY created_at DESC LIMIT 100;
```