@echo off
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0banner.ps1"
docker compose -f .\compose.yaml -p "ev-odoo-local-windows" down
docker compose -f .\compose.yaml -p "ev-odoo-local-windows" up -d

:checkloop
curl --silent --fail http://localhost:8069 >nul
if %errorlevel%==0 (
    echo Experts Vision Odoo is Running ...
    start "" "http://localhost:8069"
) else (
    timeout /t 2 >nul
    goto checkloop
)
