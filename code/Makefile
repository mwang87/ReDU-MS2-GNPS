build:
	docker build -t gnpsmetadata .

build-no-cache:
	docker build --no-cache -t gnpsmetadata .

populate:
	docker run -d -v $(PWD)/../database/:/app/database -v $(PWD)/../temp/:/app/temp --rm  gnpsmetadata /app/run_production_populate.sh

global_search:
	docker run -it -v $(PWD)/../database/:/app/database -v $(PWD)/../temp/:/app/temp --rm  gnpsmetadata /app/populate_global_search.sh

interactive:
	docker run -it -v $(PWD)/../database/:/app/database -v $(PWD)/../temp/:/app/temp -p 5006:5001 --rm --name gnpsmetadata gnpsmetadata /app/run_production_server.sh

server:
	docker run -d  -v $(PWD)/../database/:/app/database -v $(PWD)/../temp/:/app/temp -p 5005:5001 --rm --name gnpsmetadata gnpsmetadata /app/run_production_server.sh

testserver:
	docker run -it -v $(PWD)/../database/:/app/database -v $(PWD)/../temp/:/app/temp -p 5006:5001 --rm --name gnpsmetadata gnpsmetadata /app/run_server.sh

populate-test:
	docker exec -i -t gnpsmetadata /app/run_test_populate.sh

bash:
	docker run -it -v $(PWD)/../database/:/app/database -v $(PWD)/../temp/:/app/temp  -p 5006:5001 --rm --name gnpsmetadata gnpsmetadata bash

attach:
	docker exec -i -t gnpsmetadata  /bin/bash
