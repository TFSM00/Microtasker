from os import environ, path, getcwd

db_file_path = path.join(getcwd(), 'micro.db')
DEV_DB = f'sqlite:///{db_file_path}'
pg_user = environ.get("POSTGRES_USER")
pg_pass = environ.get("POSTGRES_PASSWORD")
pg_db = environ.get("POSTGRES_DB")
# 'db' is the domain name of the PGSQL db according to the docker-compose
pg_host = environ.get("PG_HOST")
pg_port = environ.get("PG_PORT")
PROD_DB = f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}'
