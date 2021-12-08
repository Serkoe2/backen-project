# ger-offer — backend

[Все репозитории команды](https://bitbucket.org/getoffer/)

[Репозиторий](https://bitbucket.org/getoffer/backend/), для запуска backend'а проекта.



## Запуск в docker-compose

При первом запуске и при инициализации/миграции Базы Данных обязателены оба скрипта!

```
docker-compose -f docker-compose.yml up --build
docker-compose exec api bash upgrade_db.sh
```



## Локальный запуск

Соединение с Базой Данных в Backend/config.py

```
cd Backend/
bash install.sh
flask run
```
