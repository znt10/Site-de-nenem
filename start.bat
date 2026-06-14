@echo off
REM Recria o container web para garantir que o .env mais recente seja carregado
docker compose up -d --force-recreate web
