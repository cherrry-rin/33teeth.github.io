# Руководство по интеграции Admin Panel и Frontend

## 1. Поток данных

### 1.1 Админ → Frontend (однонаправленный)

```
Admin редактирует услугу
        │
        ▼
API v2 (PUT /services?id=N)
        │
        ├──► ServiceService.update()
        ├──► Repository.update()  
        ├──► MySQL UPDATE
        ├──► invalidateServiceCache()
        └──► auditServiceChange()
        │
        ▼
Frontend получает новые данные при следующем запросе
```

### 1.2 Frontend → API (чтение)

```
Frontend: fetch('/php/api/public/services.php?category=Терапевт')
        │
        ▼
Публичный API проверяет is_active=1
        │
        ▼
Возвращает только активные услуги
```

## 2. Конфигурация окружения

### 2.1 .env файл
```bash
# База данных
DB_HOST=localhost
DB_NAME=33teeth_db
DB_USER=admin
DB_PASS=secure_password

# Безопасность
ADMIN_TOKEN_TTL=86400
RATE_LIMIT=100
RATE_WINDOW=60
ALLOWED_ORIGINS=https://33zub.ru,https://www.33zub.ru

# Кеш
CACHE_TTL=300
```

## 3. JavaScript клиент

### 3.1 Класс API клиента
```javascript
class ServiceClient {
    constructor(baseURL, token = null) {
        this.base = baseURL;
        this.token = token;
    }
    
    // Публичные услуги (без токена)
    async getActive(category = null) {
        const params = new URLSearchParams();
        if (category) params.set('category', category);
        
        const resp = await fetch(`${this.base}/public/services.php?${params}`);
        if (resp.status === 304) return { cached: true };
        
        const data = await resp.json();
        if (data.success && resp.headers.get('ETag')) {
            localStorage.setItem('services_etag', resp.headers.get('ETag'));
        }
        return data;
    }
    
    // Админ API (с токеном)
    async list(token) {
        return fetch(`${this.base}/v2/services.php`, {
            headers: { 'Authorization': `Bearer ${token}` }
        }).then(r => r.json());
    }
    
    async create(data, token) {
        return fetch(`${this.base}/v2/services.php`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(data)
        }).then(r => r.json());
    }
    
    async update(id, data, token) {
        return fetch(`${this.base}/v2/services.php?id=${id}`, {
            method: 'PUT',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(data)
        }).then(r => r.json());
    }
}
```

### 3.2 React хук для услуг
```javascript
// hooks/useServices.js
import { useState, useEffect } from 'react';

export function useServices(category = null) {
    const [services, setServices] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    
    useEffect(() => {
        const client = new ServiceClient('/33teeth/php/api');
        
        client.getActive(category)
            .then(data => {
                if (!data.cached) setServices(data.data || []);
            })
            .catch(err => setError(err.message))
            .finally(() => setLoading(false));
            
        // SSE для realtime обновлений
        const events = new EventSource('/33teeth/php/api/events.php');
        events.addEventListener('service.updated', () => {
            client.getActive(category).then(setServices);
        });
        
        return () => events.close();
    }, [category]);
    
    return { services, loading, error };
}
```

## 4. Безопасность

### 4.1 Заголовки безопасности (Apache)
```apache
# .htaccess в корне
<IfModule mod_headers.c>
    Header always set Strict-Transport-Security "max-age=63072000; includeSubDomains; preload"
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-Frame-Options "SAMEORIGIN"
    Header always set X-XSS-Protection "1; mode=block"
    Header always set Referrer-Policy "strict-origin-when-cross-origin"
</IfModule>
```

### 4.2 PHP-настройки
```php
// В php/config/db.php или отдельный security.php
ini_set('session.cookie_httponly', 1);
ini_set('session.cookie_secure', 1); // Только HTTPS
ini_set('session.use_strict_mode', 1);
```

## 5. Тестирование

### 5.1 Тест API endpoints
```bash
# Проверка публичного API
curl -i https://33zub.ru/33teeth/php/api/public/services.php

# Проверка админ API
curl -i -H "Authorization: Bearer $TOKEN" \
    https://33zub.ru/33teeth/php/api/v2/services.php
```

### 5.2 Health check
```bash
curl https://33zub.ru/33teeth/php/api/health.php
```

## 6. Деплой

### 6.1 Проверка перед деплоемм
- [ ] SSL сертификат установлен
- [ ] .env настроен
- [ ] Миграции выполнены
- [ ] Права на storage/cache - writable

### 6.2 Переключение на v2 API
В админке изменить `API_BASE`:
```javascript
// Было
const API_BASE = '/33teeth/php/api/';

// Стало (использует v2)
const API_BASE = '/33teeth/php/api/v2/';
```