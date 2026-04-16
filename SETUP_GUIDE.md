# IBS HI Sale Platform v4 — Setup Guide

Complete setup instructions for the FastAPI server with Pydantic models.

## Table of Contents

1. [Initial Setup](#initial-setup)
2. [Database Configuration](#database-configuration)
3. [API Key Management](#api-key-management)
4. [Starting the Server](#starting-the-server)
5. [Testing the API](#testing-the-api)
6. [Next Integration Steps](#next-integration-steps)

## Initial Setup

### Prerequisites

- Python 3.9+
- pip or conda
- SQLite3 (built-in) or PostgreSQL 13+
- Virtual environment tool (venv or conda)

### Step 1: Create Virtual Environment

```bash
cd /Users/huyenleduy/Library/CloudStorage/GoogleDrive-leduyhuyen@gmail.com/My\ Drive/IBS\ HI/Sale/sale_platform_v4

# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Expected packages:
- fastapi==0.115.0
- uvicorn==0.30.0
- pydantic==2.9.0
- psycopg2-binary==2.9.9 (for PostgreSQL support)
- google-auth==2.35.0 (for Gmail integration)
- apscheduler==3.10.4 (for task scheduling)

## Database Configuration

### Option A: SQLite (Default)

**Simplest option for development.**

```bash
# Set environment variables
export SALE_DB_PATH="./sale_platform.db"
export DB_TYPE="sqlite"

# Database will be created automatically on first run
# Ensure the directory is writable
```

SQLite features enabled:
- WAL (Write-Ahead Logging) mode for concurrent access
- Foreign key constraints enabled
- Row factory for dict-like access

### Option B: PostgreSQL (Production)

**Recommended for production environments.**

```bash
# 1. Create database
createdb ibs_hi_sale

# 2. Set environment variables
export DB_TYPE="postgresql"
export PG_DSN="postgresql://user:password@localhost:5432/ibs_hi_sale"

# 3. Verify connection
psql postgresql://user:password@localhost:5432/ibs_hi_sale -c "SELECT 1"
```

PostgreSQL features:
- Real JSONB support
- Better concurrency
- Native UUID type support
- Full-text search capabilities

## API Key Management

### Step 1: Generate API Keys

```bash
# Generate secure API keys (example using Python)
python3 -c "import uuid; print(f'Key: {uuid.uuid4().hex}')"
```

Run this 6 times to create keys for 3 tiers (2 keys each):

```
ADMIN_API_KEY_1: 8f9b4c3d5e2a1f6b9c0d3e4a5f6b7c8d
ADMIN_API_KEY_2: a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2
MANAGER_API_KEY_1: d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8
MANAGER_API_KEY_2: 9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f
VIEWER_API_KEY_1: 4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c
VIEWER_API_KEY_2: 1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d
```

### Step 2: Create .env File

```bash
cat > .env << 'EOF'
# Server Configuration
SALE_PORT=8767
API_HOST=0.0.0.0

# Database Configuration
DB_TYPE=sqlite
SALE_DB_PATH=./sale_platform.db

# PostgreSQL (if using PG)
# PG_DSN=postgresql://user:password@localhost:5432/ibs_hi_sale

# API Keys - ADMIN Tier (Full Access)
ADMIN_API_KEY_1=8f9b4c3d5e2a1f6b9c0d3e4a5f6b7c8d
ADMIN_API_KEY_2=a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2

# API Keys - MANAGER Tier (Write Access)
MANAGER_API_KEY_1=d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8
MANAGER_API_KEY_2=9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f

# API Keys - VIEWER Tier (Read-Only)
VIEWER_API_KEY_1=4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c
VIEWER_API_KEY_2=1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d

# Layer 1 Integration
IBSHI1_URL=http://localhost:3000
IBSHI1_TOKEN=

# Gmail Integration
GMAIL_CREDENTIALS_PATH=./credentials/gmail_credentials.json
GMAIL_TOKENS_DIR=./tokens/

# Features
ENABLE_EMAIL_SYNC=true
ENABLE_PM_INTEGRATION=true
ENABLE_TASK_SCHEDULING=true

# Logging
LOG_LEVEL=INFO
EOF
```

### Step 3: Secure API Keys (Production)

```bash
# 1. Use environment variables instead of .env for production
export ADMIN_API_KEY_1="<generated-key-1>"
export ADMIN_API_KEY_2="<generated-key-2>"
# ... etc

# 2. Or use a secrets manager
# AWS Secrets Manager, HashiCorp Vault, etc.

# 3. Restrict .env file permissions
chmod 600 .env
```

## Starting the Server

### Development Mode

```bash
# With auto-reload and debug logging
python -m uvicorn main:app \
  --reload \
  --host 0.0.0.0 \
  --port 8767 \
  --log-level info

# Server will start at http://0.0.0.0:8767
# Auto-reload on file changes
# Interactive docs at http://localhost:8767/docs
```

### Production Mode

```bash
# Using Gunicorn with Uvicorn workers
pip install gunicorn

gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8767 \
  --log-level info

# Or direct Uvicorn
uvicorn main:app \
  --host 0.0.0.0 \
  --port 8767 \
  --workers 4
```

### Using Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8767"]
```

```bash
docker build -t ibs-sale-platform .
docker run -p 8767:8767 \
  -e DB_TYPE=sqlite \
  -e SALE_DB_PATH=/data/sale_platform.db \
  -e ADMIN_API_KEY_1=<key> \
  -v $(pwd)/data:/data \
  ibs-sale-platform
```

## Testing the API

### 1. Health Check (No Auth Required)

```bash
curl http://localhost:8767/health

# Expected response:
{
  "status": "ok",
  "version": "1.0.0",
  "port": 8767,
  "db_type": "sqlite",
  "email_sync_enabled": true,
  "pm_integration_enabled": true
}
```

### 2. Database Check (No Auth Required)

```bash
curl http://localhost:8767/health/db

# Expected response:
{
  "status": "ok",
  "db_type": "sqlite",
  "connected": true,
  "timestamp": "2026-04-15T10:30:00"
}
```

### 3. Create a Customer (With MANAGER Key)

```bash
curl -X POST \
  -H "X-API-Key: d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ACME Corporation",
    "code": "ACME001",
    "country": "Vietnam",
    "region": "Ho Chi Minh City",
    "status": "ACTIVE"
  }' \
  http://localhost:8767/api/v1/customers

# Expected response:
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "created",
  "message": "Customer 'ACME Corporation' created successfully"
}
```

### 4. List Opportunities (With Any Valid Key)

```bash
curl -H "X-API-Key: 4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c" \
  http://localhost:8767/api/v1/opportunities

# Expected response:
{
  "total": 0,
  "opportunities": [],
  "limit": 50,
  "offset": 0
}
```

### 5. Interactive API Documentation

Open browser: `http://localhost:8767/docs`

- Swagger UI with all endpoints
- Try-it-out functionality
- Request/response schemas
- API key authentication testing

## Accessing Interactive Docs

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: `http://localhost:8767/docs`
- **ReDoc**: `http://localhost:8767/redoc`
- **OpenAPI Schema**: `http://localhost:8767/openapi.json`

## Next Integration Steps

### 1. Database Initialization

Execute the schema from the System Design document to create tables:

```bash
# For SQLite
sqlite3 sale_platform.db < schema.sql

# For PostgreSQL
psql -d ibs_hi_sale < schema_pg.sql
```

### 2. Enable Router Endpoints

Uncomment router includes in `main.py`:

```python
from .routers import (
    health, customers, opportunities, emails, tasks,
    dashboard, mailboxes, users, pm_integration
)

# Include routers
app.include_router(customers.router, prefix="/api/v1", dependencies=auth_dep)
app.include_router(opportunities.router, prefix="/api/v1", dependencies=auth_dep)
# ... etc
```

### 3. Gmail Integration

1. Set up OAuth2 credentials in Google Cloud Console
2. Place credentials JSON at `./credentials/gmail_credentials.json`
3. Configure `GMAIL_CREDENTIALS_PATH` and `GMAIL_TOKENS_DIR` in `.env`
4. Implement email sync worker

### 4. PM Integration

1. Set up webhook receivers for PM system events
2. Implement reverse sync from PM → Sale platform
3. Configure `IBSHI1_URL` and `IBSHI1_TOKEN` in `.env`
4. Test 2-way synchronization

### 5. Deploy to Production

```bash
# 1. Use production-grade server (Gunicorn + Uvicorn)
# 2. Configure reverse proxy (Nginx)
# 3. Enable HTTPS/TLS
# 4. Set up logging and monitoring
# 5. Configure database backups
# 6. Implement rate limiting and throttling
# 7. Add request/response logging
```

## Monitoring and Logging

### View Logs

```bash
# Development mode logs to console
# For file logging, update main.py to add file handler

# Example: Check for startup issues
tail -f /tmp/sale_platform.log
```

### Health Monitoring

```bash
# Set up health check for load balancer
while true; do
  curl -f http://localhost:8767/health || exit 1
  sleep 30
done
```

### Database Monitoring

```bash
# Monitor database file size (SQLite)
du -sh sale_platform.db

# Check PostgreSQL connections
psql -d ibs_hi_sale -c "SELECT count(*) FROM pg_stat_activity;"
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 8767
lsof -i :8767

# Kill process
kill -9 <PID>

# Or use different port
export SALE_PORT=8768
```

### Database Connection Error

```bash
# Check SQLite file exists
ls -la sale_platform.db

# Check PostgreSQL connection
psql postgresql://user:password@localhost:5432/ibs_hi_sale -c "SELECT 1"

# Verify env variables
echo $DB_TYPE $PG_DSN
```

### API Key Not Working

```bash
# Verify key is in config.py API_KEYS dict
# Check header name is exactly "X-API-Key"
# Verify key is not expired/revoked
curl -v -H "X-API-Key: test-key" http://localhost:8767/api/v1/customers
```

## File Overview

| File | Purpose |
|------|---------|
| `requirements.txt` | Python package dependencies |
| `config.py` | Environment variables and configuration |
| `database.py` | SQLite/PostgreSQL connection helper |
| `auth.py` | API key authentication (3-tier) |
| `main.py` | FastAPI app initialization and startup |
| `models/*.py` | Pydantic request/response schemas |
| `routers/*.py` | API endpoint handlers (CRUD, business logic) |
| `README.md` | API documentation and overview |
| `SETUP_GUIDE.md` | This file |

## Support

For detailed API documentation, see `README.md`.

For system design and database schema, see System Design document:
`/Users/huyenleduy/Documents/Claude/Projects/IBS HI/IBS HI/Sale_Phase1_System_Design_and_Dev_Plan.md`
