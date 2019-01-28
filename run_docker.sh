docker rm gnpsmetadatafoodomics
docker run -d  -p 5021:5001 --name gnpsmetadatafoodomics gnpsmetadatafoodomics /app/run_production_server.sh
#docker run -it -p 5021:5001 --name gnpsmetadatafoodomics gnpsmetadatafoodomics /app/run_server.sh
#docker run -it -p 5000:5001 --name gnpsmetadatafoodomics gnpsmetadatafoodomics bash
