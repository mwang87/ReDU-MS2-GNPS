docker rm gnpsmetadata
#docker run -d  -p 5000:5001 --name gnpsmetadata gnpsmetadata /app/run_production_server.sh
#docker run -d -p 5000:5001 --name gnpsmetadata gnpsmetadata /app/run_server.sh
docker run -it -p 5000:5001 --name gnpsmetadata gnpsmetadata /bin/bash
