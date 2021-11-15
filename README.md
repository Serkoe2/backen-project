<h4>запуск в Docker compose</h4>
При первом запуске и при инициализации/миграции Базы Данных обязателены оба скрипта!
```
docker-compose -f docker-compose.yml up --build
docker-compose exec api bash upgrade_db.sh
```
<h4>Локальный запуск</h4>
Backend
Соединение с Базой Данных в Backend/config.py
```
cd Backend/
bash install.sh
flask run
```

