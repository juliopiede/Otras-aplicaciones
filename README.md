# Gestor de licitaciones Bittácora

Aplicación MVP completa (backend API) para gestionar licitaciones con filtros, scoring y estados de seguimiento.

## 1) Requisitos
- Python 3.12+
- PostgreSQL 16+
- (Opcional) Docker + Docker Compose

## 2) Instalación local (sin Docker)
```bash
cp backend/.env.example backend/.env
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements-dev.txt
```

## 3) Variables de entorno
Definir en `backend/.env`:
- `APP_ENV`
- `APP_HOST`
- `APP_PORT`
- `DATABASE_URL`

Ejemplo disponible en `backend/.env.example`.

## 4) Migraciones y datos de prueba
```bash
export DATABASE_URL=postgresql://bittacora:bittacora@localhost:5432/bittacora
python backend/scripts/migrate.py
```
Esto aplica automáticamente todas las migraciones de `backend/migrations/*.sql` en orden.

## 5) Ejecutar en local
```bash
uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port 8000
```

## 6) Comandos útiles
```bash
make install-dev
make test
make run
```

## 7) URL local exacta
- Panel web MVP: `http://localhost:8000`
- API docs (Swagger): `http://localhost:8000/docs`

## 8) Despliegue en producción (guía)
1. Provisionar VPS (ej. Hetzner) con Docker y dominio.
2. Configurar DNS del dominio apuntando a la IP del VPS.
3. Levantar stack con `docker compose up -d --build`.
4. Las migraciones se aplican automáticamente con el servicio `migrate` al hacer `docker compose up`.
5. Poner reverse proxy (Nginx/Caddy) con TLS (Let's Encrypt).
6. Configurar backups de Postgres y monitorización.

## 9) Pasos pendientes para publicar en dominio real
- Comprar/configurar dominio.
- Crear registros DNS A/AAAA.
- Instalar y configurar proxy HTTPS.
- Configurar variables de entorno de producción.
- Activar observabilidad (logs, alertas, uptime checks).
