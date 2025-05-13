#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$DB_USER" <<-EOSQL
    DO
    \$do\$
    BEGIN
        IF NOT EXISTS (
            SELECT FROM pg_catalog.pg_user WHERE usename = '$DB_USER'
        ) THEN
            CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
        END IF;
    END
    \$do\$;

    CREATE DATABASE $DB_NAME OWNER $DB_USER;
    GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
EOSQL
