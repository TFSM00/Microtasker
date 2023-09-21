docker login
docker pull tfsm00/flask-nginx-postgres:latest
docker compose up --build -d --envfile env.txt