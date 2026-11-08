# Integration candidates

Это **инструкции кандидатов**, не установленные плагины, запущенные агенты или готовые боевые конфигурации.

| Компонент | Назначение | Статус |
|---|---|---|
| [Uptime Kuma](uptime-kuma/README.md) | Контроль доступности инфраструктуры | Protocol ready; NOT RUN |
| [Docling](docling/README.md) | Обработка сложных документов | Protocol ready; NOT RUN |
| [Browser Use](browser-use/README.md) | Browser E2E / agent | Protocol ready; NOT RUN |
| [Crawl4AI](crawl4ai/README.md) | Structured public-web extraction | Protocol ready; NOT RUN |

## Базовые правила

- Изоляция: отдельный тестовый контейнер/VM/виртуальное окружение; никакого автоматического доступа к продакшн n8n и приватным данным.
- Перед тестом закрепить версию и проверить `LICENSE` / security advisories / README.
- Команды из README — **процедуры для отдельного ручного запуска**, не доказательство выполнения.
- Не запускать `curl | bash` в production; не копировать ключи в репозиторий.
- Протокол и критерии: [tool evaluation](../reference/tool-evaluations/2026-11-08-first-wave.md).
