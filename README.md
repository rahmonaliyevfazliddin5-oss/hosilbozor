# HosilBozor — O'zbekiston Agrar Bozor Web Platformasi

> Fermerlar, ulgurji xaridorlar va yuk tashuvchi haydovchilarni to'g'ridan-to'g'ri bog'lovchi, o'rtakashlarni chetlab o'tuvchi va narx shaffofligini ta'minlovchi platforma.

---

## 🏗 Arxitektura va Texnologiyalar

- **Backend:** Python 3.12 / 3.13, FastAPI (Modular Monolith), SQLAlchemy 2, Alembic
- **Database:** PostgreSQL 16 + PostGIS (spatial geo queries), SQLite (test/offline dev)
- **Cache & Jobs:** Redis 7, Celery + Celery Beat
- **Frontend & Mini App:** Next.js (App Router, TypeScript, Tailwind) & React Telegram Mini App
- **Bot:** aiogram 3 (Webhook & Polling)
- **Ko'ptillilik (i18n):** O'zbekcha (Lotin, standart), Ўзбекча (Кирилл), Русский

---

## 🚀 10 Daqiqada Tezkor O'rnatish (Quickstart)

### 1. Docker Compose orqali (Tavsiya etiladi)

```bash
# Repository'ni klon qiling yoki scratch katalogiga kiring
cd C:\Users\rahmo\.gemini\antigravity\scratch\hosilbozor

# .env faylini nusxalang
cp .env.example .env

# Konteynerlarni ko'taring (PostgreSQL+PostGIS, Redis, FastAPI Backend)
docker compose up -d --build

# API holatini tekshiring
curl http://localhost:8000/health
```

### 2. Mahalliy Python muhitida (Local Development)

```bash
cd backend

# Virtual muhit yaratish va aktivlashtirish
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# Bog'liqliklarni o'rnatish
pip install -r requirements.txt

# Migratsiyalarni ishga tushirish
alembic upgrade head

# FastAPI serverini ishga tushirish
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- **Swagger / OpenAPI Dokumentatsiyasi:** [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)
- **ReDoc Dokumentatsiyasi:** [http://localhost:8000/api/v1/redoc](http://localhost:8000/api/v1/redoc)

---

## 🧪 Testlarni Ishga Tushirish va Coverage

Barcha unit va integratsion testlar 100% mustaqil in-memory SQLite bazasida xavfsiz ishlaydi:

```bash
cd backend
pytest -v --cov=app --cov-report=term-missing
```

Hozirgi holat: **22 ta test to'liq o'tgan (100% pass), test qamrovi (coverage): 94%**.

---

## 📂 Loyiha Tuzilishi

```text
hosilbozor/
├── .github/workflows/ci.yml       # GitHub Actions avtomatik CI pipeline
├── .env.example                   # Muhit o'zgaruvchilari shabloni
├── .gitignore
├── docker-compose.yml             # PostGIS, Redis, Backend xizmatlari
├── README.md                      # Loyiha qo'llanmasi
└── backend/
    ├── alembic/                   # Ma'lumotlar bazasi migratsiyalari
    ├── app/
    │   ├── api/v1/                # REST API routerlari (auth, users, meta, ...)
    │   ├── core/                  # Sozlamalar, xavfsizlik (JWT), DB, i18n
    │   ├── i18n/locales/          # uz_latn.json, uz_cyrl.json, ru.json
    │   ├── models/                # 20+ ta SQLAlchemy 2 PostGIS modellari
    │   ├── repositories/          # Ma'lumotlar bazasi abstraksiyalari
    │   ├── schemas/               # Pydantic v2 validatsiya sxemalari
    │   ├── services/              # Biznes mantiq (Auth, SMS, Escrow)
    │   └── main.py                # FastAPI asosiy kirish nuqtasi
    └── tests/                     # Pytest integratsion testlar to'plami
```
