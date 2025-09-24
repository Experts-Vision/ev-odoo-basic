@echo off
echo This will create a Postgres Docker container under namespace ev-odoo-dev-windows
docker compose -f .\compose.yaml -p "ev-odoo-dev-windows" down
docker compose -f .\compose.yaml -p "ev-odoo-dev-windows" up -d
