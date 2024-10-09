#!/bin/bash
set -e

until psql "postgresql://$POSTGRES_USER@:5432" -c '\q'; do
  >&2 echo "Postgres is unavailable - waiting..."
  sleep 1
done

psql -v ON_ERROR_STOP=1 "postgresql://$POSTGRES_USER@:5432" <<-EOSQL
  DROP DATABASE IF EXISTS gn_monitor;
  DROP USER IF EXISTS dev;
  CREATE USER dev WITH PASSWORD 'dev_pass';
  CREATE DATABASE gn_monitor;
  GRANT ALL PRIVILEGES ON DATABASE gn_monitor TO dev;
  GRANT USAGE ON SCHEMA public TO dev;
  GRANT CREATE ON SCHEMA public TO dev;
EOSQL
