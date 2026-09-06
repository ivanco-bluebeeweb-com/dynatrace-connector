# Dynatrace Connector — Connector Discovery

**Vendor API Baseline:** https://dynatrace.com

## Архитектура API
- **Базовый адрес:** `https://<environment-id>.live.dynatrace.com/api/v2`
- **Протокол:** REST / HTTPS (JSON)
- **Аутентификация:** Dynatrace API Token (Authorization: Api-Token <token>)
- **Ключевые эндпоинты:**
  - проблемы и инциденты (/problems)
  - сервисы и сущности инфраструктуры (/entities)
  - метрики (/metrics)
- **Тестовая точка проверки подключения:** `GET /api/v2/metrics`.
