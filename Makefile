start_db:
	docker run -d \
	--name getoffer_db \
	-e POSTGRES_PASSWORD=qwerty \
	-e POSTGRES_USER=starter_kit \
	-p 5432:5432 \
	-v "/Users/s.timoshenkov/Desktop/Projects/GetOffer/backend/postgres_data":/var/lib/postgresql/data \
	postgres 

.PHONY: start_db