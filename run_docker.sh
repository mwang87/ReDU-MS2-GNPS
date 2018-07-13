docker rm gnpsmetadata
docker run -d -p 5001:5000 --name gnpsmetadata gnpsmetadata /app/run_server.sh
#docker run -it -p 5000:5000 --name gnpsmetadata gnpsmetadata bash
