# 33teeth - Admin Panel & Frontend Integration

## Architecture

```
Admin Panel (vHd5Gz7qKl/) ←→ API v2 (/php/api/v2/) ←→ MySQL
       ↑                            ↑
       └── Session/Bearer Token     └── Public API (/php/api/public/)
                                          ↑
                                          └── Frontend (no auth)
```

## Components Created

| Component | Path | Purpose |
|-----------|------|---------|
| Public API | `/php/api/public/services.php` | Read-only frontend access |
| API v2 | `/php/api/v2/services.php` | Admin CRUD with layers |
| Repository | `/php/app/Repository/ServiceRepository.php` | Data access layer |
| Service | `/php/app/Service/ServiceService.php` | Business logic |
| Cache | `/php/api/cache-helper.php` | File-based caching |
| CORS | `/php/app/Middleware/CorsMiddleware.php` | CORS + token auth |
| Security | `/php/app/Middleware/SecurityMiddleware.php` | Rate limiting |
| Events | `/php/api/events.php` | SSE for realtime |
| Health | `/php/api/health.php` | System status |
| Audit | `/php/app/Middleware/AuditLogger.php` | Action logging |

## Setup

1. **Create cache directory:**
```bash
mkdir php/storage/cache
chmod 755 php/storage/cache
```

2. **Run migrations:**
```bash
mysql -u DB_USER -p DB_NAME < php/sql/migration_services.sql
mysql -u DB_USER -p DB_NAME < php/sql/migration_audit_log.sql
```

3. **Configure `.env`:**
```bash
cp .env.example .env
# Edit values
```

## Security Features

- HTTPS enforced
- Bearer token auth (24h expiry)
- Rate limiting (100 req/min/IP)
- CORS whitelist
- CSRF protection
- Audit logging all actions

## API Usage

### Public (Frontend)
```
GET /php/api/public/services.php?category=Терапевт
```

### Admin
```
GET /php/api/v2/services.php
Authorization: Bearer {token}
```

## Documentation

- `ARCHITECTURE.md` - Full architecture
- `SECURITY.md` - Security setup guide
- `INTEGRATION_GUIDE.md` - Integration examples
- `API_DOCS.md` - Complete API reference