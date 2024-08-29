#!/bin/bash
set -e

until psql "postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@:5432" -c '\q'; do
  >&2 echo "Postgres is unavailable - waiting..."
  sleep 1
done

psql -v ON_ERROR_STOP=1 "postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@:5432" <<-EOSQL
  DROP DATABASE IF EXISTS gn_monitor;
  DROP USER IF EXISTS dev;
  CREATE USER dev WITH PASSWORD 'dev';
  CREATE DATABASE gn_monitor;
  GRANT ALL PRIVILEGES ON DATABASE gn_monitor TO dev;
EOSQL
