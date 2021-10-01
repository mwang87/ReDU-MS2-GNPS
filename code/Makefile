build:
	docker build -t gnpsmetadata .

build-no-cache:
	docker build --no-cache -t gnpsmetadata .

populate_metadata:
	docker run -it -v $(PWD)/../database/:/app/database -v $(PWD)/../temp/:/app/temp --rm  gnpsmetadata /app/utilities/run_production_populate.sh

populate_identification:
	docker run -it -v $(PWD)/../database/:/app/database -v $(PWD)/../temp/:/app/temp --rm  gnpsmetadata /app/utilities/populate_identifications.sh

global_search:
	docker run -it -v $(PWD)/../database/:/app/database -v $(PWD)/../temp/:/app/temp --rm  gnpsmetadata /app/run_redu_librarysearch.sh

interactive:
	docker run -it -v $(PWD)/../database/:/app/database -v $(PWD)/../temp/:/app/temp -p 5006:5001 --rm --name gnpsmetadata gnpsmetadata /app/run_production_server.sh

server:
	docker run -d  -v $(PWD)/../database/:/app/database -v $(PWD)/../temp/:/app/temp -p 5005:5001 --rm --name gnpsmetadata gnpsmetadata /app/run_production_server.sh

testserver:
	docker run -it -v $(PWD)/../database/:/app/database -v $(PWD)/../temp/:/app/temp -p 5006:5001 --rm --name gnpsmetadata gnpsmetadata /app/run_server.sh

populate-test:
	docker run -it -v $(PWD)/../database/:/app/database -v $(PWD)/../temp/:/app/temp --rm --name gnpsmetadata gnpsmetadata /app/utilities/run_test_populate.sh

bash:
	docker run -it -v $(PWD)/../database/:/app/database -v $(PWD)/../temp/:/app/temp  -p 5006:5001 --rm --name gnpsmetadata gnpsmetadata bash

#Docker Compose
server-compose-interactive:
	docker-compose build
	docker-compose --compatibility up 

server-compose-background:
	docker-compose build
	docker-compose --compatibility up -d 

attach:
	docker exec -i -t code_redu-ms2-populate_1  /bin/bash