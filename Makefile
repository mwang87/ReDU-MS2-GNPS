build:
	docker build -t gnpsmetadata .
interactive:
	docker run -it  -p 5005:5001 --rm --name gnpsmetadata gnpsmetadata /app/run_production_server.sh
server:
	docker run -d  -p 5005:5001 --rm --name gnpsmetadata gnpsmetadata /app/run_production_server.sh
bash:
	docker run -it  -p 5005:5001 --rm --name gnpsmetadata gnpsmetadata bash
