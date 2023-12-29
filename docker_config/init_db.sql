SELECT 'CREATE DATABASE ws_demo'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'ws_demo')\gexec

CREATE USER ws_demo WITH PASSWORD 'ws_demo' CREATEDB;
