# 🚨 Incident Tracker API

Простой сервис на Flask для учёта инцидентов (проблемы от операторов, мониторинга и партнёров).
Все данные хранятся в SQLite, настройки — в `config.json`.

---

## ▶️ Как запустить

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

2. Запустите сервер:
   ```bash
   python app.py
   ```
   Сервис будет доступен на `http://localhost:5000`.

> При первом запуске автоматически создастся файл базы `incidents.db`.

---

## 🌐 Эндпоинты

### `POST /incidents/create`
Создать новый инцидент.

```bash
curl -X POST http://localhost:5000/incidents/create \
  -H "Content-Type: application/json" \
  -d '{"description": "Самокат #42 не в сети", "type": "critical", "status": "ongoing", "source": "monitoring"}'
```

### `GET /incidents`
Получить список всех инцидентов (с опциональным фильтром по статусу).

```bash
# Все инциденты
curl http://localhost:5000/incidents

# Только новые
curl "http://localhost:5000/incidents?status=new"
```

### `PATCH /incidents/&lt;id&gt;/status`
Обновить статус инцидента.

```bash
curl -X PATCH http://localhost:5000/incidents/1/status \
  -H "Content-Type: application/json" \
  -d '{"status": "resolved"}'
```

### `GET /incidents/&lt;id&gt;`
Получить инцидент по id.

```bash
# Инциденты
curl http://localhost:5000/incidents/1
```

> Возможные типы: `ordinary`, `important`, `exclusive`, `critical`
> Возможные статусы: `new`, `ongoing`, `resolved`, `closed`
> Возможные источники: `operator`, `monitoring`, `partner`

