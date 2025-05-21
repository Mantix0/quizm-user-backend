#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    DO
    \$do\$
    BEGIN
        IF NOT EXISTS (
            SELECT FROM pg_catalog.pg_user WHERE usename = '$POSTGRES_USER'
        ) THEN
            CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';
        END IF;

        IF NOT EXISTS (
            SELECT FROM pg_database WHERE datname = '$POSTGRES_DB'
        ) THEN
            CREATE DATABASE $POSTGRES_DB OWNER $POSTGRES_USER;
        END IF;

        GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER;
    END
    \$do\$;
EOSQL
