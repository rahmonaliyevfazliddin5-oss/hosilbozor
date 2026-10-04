# HosilBozor — Deploy va Ishga Tushirish Qo'llanmasi (Deployment Guide)

Ushbu qo'llanma **HosilBozor** platformasini **Render.com** bulut xizmatida hamda **Docker Compose** orqali serverda ishga tushirish bo'yicha to'liq ko'rsatmalarni o'z ichiga oladi.

---

## 1. Render.com da Deploy Qilish

Render platformasida HosilBozor arxitekturasi quyidagi servislarga bo'linadi:

```
┌─────────────────────────────────────────────────────────────┐
│                      RENDER CLOUD                           │
│                                                             │
│  1. HosilBozor Web (Next.js)      [Web Service / Node.js]   │
│  2. HosilBozor API (FastAPI)      [Web Service / Python]    │
│  3. HosilBozor Database           [PostgreSQL + PostGIS]    │
│  4. HosilBozor Redis              [Redis Service]           │
│  5. HosilBozor Celery Worker      [Background Worker]       │
└─────────────────────────────────────────────────────────────┘
```

### A. Ma'lumotlar Bazasi (PostgreSQL + PostGIS)
1. Render Dashboard'da **New -> PostgreSQL** yarating:
   - Name: `hosilbozor-db`
   - Database: `hosilbozor`
   - User: `hosilbozor_user`
   - Region: `Frankfurt (EU Central)`
2. PostGIS kengaytmasini yoqish:
   Render PostgreSQL terminalida quyidagi buyruqni bajaring:
   ```sql
   CREATE EXTENSION IF NOT EXISTS postgis;
   ```
3. `Internal Database URL`ni nusxalab oling (Backend uchun).

---

### B. Redis Kesh va Navbat Servisi
1. **New -> Redis** yarating:
   - Name: `hosilbozor-redis`
   - Maxmemory Policy: `allkeys-lru`
2. `Internal Redis URL`ni nusxalab oling (`redis://...`).

---

### C. Backend API (FastAPI Web Service)
1. **New -> Web Service** tanlang va GitHub repository'ni ulang:
   - Name: `hosilbozor-api`
   - Environment: `Python 3`
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt && alembic upgrade head && python scripts/seed.py`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 4`
2. **Environment Variables** bo'limida quyidagilarni kiriting:
   ```env
   PROJECT_NAME=HosilBozor
   ENVIRONMENT=production
   SECRET_KEY=generate_a_secure_random_64_character_hex_key
   DATABASE_URL=postgres://hosilbozor_user:password@hostname/hosilbozor
   REDIS_URL=redis://hostname:6379
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_from_botfather
   BACKEND_CORS_ORIGINS=["https://hosilbozor.onrender.com","https://hosilbozor.uz"]
   ```

---

### D. Frontend Web App (Next.js Web Service)
1. **New -> Web Service** tanlang:
   - Name: `hosilbozor-web`
   - Environment: `Node`
   - Root Directory: `web`
   - Build Command: `npm install && npm run build`
   - Start Command: `npm start`
2. **Environment Variables**:
   ```env
   NEXT_PUBLIC_API_URL=https://hosilbozor-api.onrender.com/api/v1
   ```

---

## 2. Docker Compose Orqali Serverda (VPS) Ishga Tushirish

Serverda (Ubuntu 22.04 / 24.04) birgina buyruq bilan butun ekotizimni ishga tushirish:

### 1. Repozitoriyni yuklash va `.env` faylini sozlash:
```bash
git clone https://github.com/your-org/hosilbozor.git
cd hosilbozor
cp .env.example .env
```

### 2. Docker Compose konteynerlarini ko'tarish:
```bash
docker compose up -d --build
```

### 3. Migratsiya va Real Ma'lumotlarni yuklash:
```bash
docker compose exec backend alembic upgrade head
docker compose exec backend python scripts/seed.py
```

### 4. Holatni tekshirish:
```bash
docker compose ps
curl http://localhost:8000/api/v1/auth/health
```

Barcha servislar (FastAPI API, PostgreSQL PostGIS, Redis, Next.js Web) avtomatik ishlaydi!
