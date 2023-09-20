from os import path, getcwd

db_file_path = path.join(getcwd(), 'micro.db')
DEV_DB = f'sqlite:///{db_file_path}'
pg_user = 'admin'
pg_pass = 'admin'
pg_db = 'micro'
# 'db' is the domain name of the PGSQL db according to the docker-compose
pg_host = 'db'
pg_port = 5432
PROD_DB = f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}'
