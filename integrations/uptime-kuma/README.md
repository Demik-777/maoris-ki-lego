# Uptime Kuma — проверка для MDL

- Upstream: https://github.com/louislam/uptime-kuma
- Source license according to GitHub API (2026-11-08): MIT; stars: 93 366.
- Задача: надзор за доступностью n8n, тестовых приложений и API, уведомления Telegram.
- Статус: **README reviewed, not installed / not run**. Не заменяет full E2E или бэкапы.

## Подготовка теста

Использовать отдельную VM с Docker или отдельный тестовый Docker host; не запускать на рабочем n8n без отдельного техрешения. Проверить актуальные Docker инструкции upstream. Не выставлять dashboard в публичный интернет без защитного периметра.

```bash
docker run -d --name mdl-uptime-kuma-test \
  --restart=no -p 127.0.0.1:13001:3001 \
  -v mdl-uptime-kuma-test-data:/app/data \
  louislam/uptime-kuma:2
docker ps --filter name=mdl-uptime-kuma-test
curl -I http://127.0.0.1:13001
```

## Проверка и критерии

1. Открыть `http://127.0.0.1:13001` только из тестовой среды, создать локального администратора.
2. Добавить тестовый HTTP endpoint, убедиться в переходе UP → DOWN → UP.
3. Подключить **отдельного тестового Telegram-бота** через UI, убедиться в DOWN и RECOVERY сообщениях.
4. Проверить устойчивость состояния после restart, расход RAM и свободное место.
5. Документировать шифрование/backup, auth, доступы. Не вводить реальный токен бота в Git.
6. Удаление тестового контейнера (без удаления volume по умолчанию):

```bash
docker rm -f mdl-uptime-kuma-test
```

PASS = HTTP доступен локально, надёжные Telegram DOWN/RECOVERY, восстановление после рестарта, приемлемая нагрузка. Тест пока **не выполнялся**.
