# HosilBozor — O'zbekiston Qishloq Xo'jaligi Raqamli Birjasi (Agri-Marketplace)

> Fermerlar, ulgurji xaridorlar va yuk tashuvchi haydovchilarni to'g'ridan-to'g'ri bog'lovchi, o'rtakash dallollarni chetlab o'tuvchi, xavfsiz Escrow to'lovi va logistika optimizatsiyasiga ega agrar ekotizim.

---

## 🏗 Arxitektura va Texnologik Stack

- **Backend:** Python 3.12 / 3.13, FastAPI (Modular Monolith), SQLAlchemy 2, Alembic
- **Database:** PostgreSQL 16 + PostGIS (spatial geo queries / radius qidiruvi), SQLite (test & dev)
- **Kesh & Asinxron Navbat:** Redis 7, Celery + Celery Beat
- **Web App:** Next.js 14 (App Router), TypeScript, Tailwind CSS, TanStack Query
- **Telegram Bot & TMA:** aiogram 3 (Webhook & Polling), HTML5/React Telegram Mini App (mijozda WebP siqish <150KB, offline qoralama)
- **Xavfsiz To'lov (Escrow):** Payme & Click adapterlari + Mahalliy Mock Escrow Sandbox simulyatori
- **Ko'ptillilik (i18n):** O'zbekcha (Lotin, standart), Ўзбекча (Кирилл), Русский

---

## 🚀 10 Daqiqada Tezkor Ishga Tushirish (Quickstart)

### 1. Docker Compose orqali (Tavsiya etiladi)

```bash
# Repozitoriy katalogiga kiring
cd C:\Users\rahmo\.gemini\antigravity\scratch\hosilbozor

# Muhit o'zgaruvchilarini nusxalang
cp .env.example .env

# PostGIS, Redis va Backend konteynerlarini ko'taring
docker compose up -d --build

# Baza migratsiyasini bajarish va real O'zbekiston ma'lumotlarini yuklash
docker compose exec backend alembic upgrade head
docker compose exec backend python scripts/seed.py
```

### 2. Mahalliy Rivojlantirish (Local Development)

#### Backend (FastAPI):
```bash
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
python scripts/seed.py         # Real ekinlar, hududlar va test akkauntlarini yuklash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- **Interaktiv API Hujjatlari:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc Hujjatlari:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

#### Web Platforma (Next.js):
```bash
cd web
npm install
npm run dev
```
- **Web Portal:** [http://localhost:3000](http://localhost:3000)
- **Hosil Bozori & Escrow:** [http://localhost:3000/listings](http://localhost:3000/listings)
- **Teskari Auksion Doskasi:** [http://localhost:3000/demand](http://localhost:3000/demand)
- **Admin & Arbitraj Paneli:** [http://localhost:3000/admin](http://localhost:3000/admin)

#### Telegram Bot:
```bash
cd backend
python -m bot.bot
```
- **Telegram Mini App:** `tma/index.html` (Mijozda siqish, offline localStorage saqlash)

---

## 🔑 Test Hisoblari (Parol barchasi uchun: `HosilBozor2026!`)

| Rol | Telefon | Foydalanuvchi | Tavsif |
| :--- | :--- | :--- | :--- |
| **Admin** | `+998900000001` | Bosh Nazoratchi | KPI boshqaruvi, foydalanuvchilarni tasdiqlash, nizolar arbitraji |
| **Fermer** | `+998901112233` | Rustam Yoqubov | Chinoz Agrogurux, 12t pomidor, 8.5t bodring |
| **Fermer** | `+998902223344` | Bahodir Mirzayev | Samarqand Zarafshon Agro, 25t kartoshka, 40t piyoz |
| **Xaridor** | `+998904445566` | Bobur Savdogar | Korzinka Ulgurji Ta'minot, Escrow buyurtmalari |
| **Haydovchi**| `+998907778899`| Davron Haydovchi | Isuzu Sovutgichli 5t (`01 A 777 AA`), 6 xonali kod bilan yetkazish |

---

## 🧪 Avtomatlashtirilgan Testlar va Tezlik Sinovi

### 1. Pytest Test To'plami (50 ta test, 91% qamrov)
```bash
cd backend
pytest -v --cov=app --cov-report=term-missing
```
```
collected 50 items
tests/test_admin.py (4 tests) PASSED
tests/test_auth.py (7 tests) PASSED
tests/test_bot_flows.py (5 tests) PASSED
tests/test_demand.py (1 test) PASSED
tests/test_escrow.py (4 tests) PASSED
tests/test_i18n.py (4 tests) PASSED
tests/test_listings.py (5 tests) PASSED
tests/test_logistics.py (1 test) PASSED
tests/test_meta_and_rbac.py (2 tests) PASSED
tests/test_orders.py (4 tests) PASSED
tests/test_prices.py (4 tests) PASSED
tests/test_users.py (9 tests) PASSED
======================= 50 passed in 7.13s =======================
TOTAL COVERAGE: 91%
```

### 2. API Yuklama va Latency Sinovi (p95 < 300 ms SLA)
```bash
cd backend
python scripts/load_test.py
```
- `Listings API`: **15.48 ms** (Talab: < 300 ms) ✅
- `Daily Prices API`: **9.13 ms** (Talab: < 300 ms) ✅
- `Crop Taxonomy API`: **4.40 ms** (Talab: < 300 ms) ✅
- `Regions & Districts API`: **6.97 ms** (Talab: < 300 ms) ✅

---

## 📚 Qo'shimcha Hujjatlar

- 📖 **[DEMO_SCRIPT.md](DEMO_SCRIPT.md)** — Bosqichma-bosqich jonli taqdimot va qabul mezonlari ssenariysi.
- 🛡️ **[docs/SECURITY_AUDIT.md](docs/SECURITY_AUDIT.md)** — OWASP Top 10 xavfsizlik auditi va Escrow kafolat mexanizmi.
- ☁️ **[DEPLOYMENT.md](DEPLOYMENT.md)** — Render.com va Linux VPS da deploy qilish bo'yicha to'liq qo'llanma.

---

## 📂 Loyiha Tuzilishi (Monorepo)

```text
hosilbozor/
├── .github/workflows/ci.yml       # GitHub Actions CI pipeline
├── .env.example                   # Muhit o'zgaruvchilari
├── docker-compose.yml             # PostGIS, Redis, Backend xizmatlari
├── README.md                      # Asosiy qo'llanma
├── DEPLOYMENT.md                  # Render & Cloud deploy yo'riqnomasi
├── DEMO_SCRIPT.md                 # 4 ta rol bo'yicha jonli demo ssenariysi
├── docs/
│   └── SECURITY_AUDIT.md          # OWASP Top 10 xavfsizlik auditi
├── backend/
│   ├── alembic/                   # Migratsiyalar
│   ├── app/
│   │   ├── api/v1/endpoints/      # auth, listings, prices, demand, orders, logistics, payments, admin
│   │   ├── core/                  # config, database, geo, i18n, security
│   │   ├── models/                # 20+ SQLAlchemy modellari
│   │   ├── repositories/          # CRUD & SQL aggregatsiya
│   │   ├── schemas/               # Pydantic v2 validatsiya
│   │   ├── services/              # Biznes mantiq, Escrow adapterlari (Mock, Payme, Click)
│   │   └── main.py                # FastAPI ilovasi
│   ├── bot/                       # aiogram 3 Telegram bot kodi
│   ├── scripts/
│   │   ├── seed.py                # O'zbekiston agrar hududlari bo'yicha real ma'lumotlar
│   │   └── load_test.py           # p95 tezlik va yuklama testi
│   └── tests/                     # 50 ta pytest testlari
├── tma/
│   └── index.html                 # Telegram Mini App (WebP siqish, offline qoralama)
└── web/
    ├── src/app/                   # Next.js 14 App Router sahifalari
    │   ├── page.tsx               # Landing sahifa (Live narxlar, tavsiyalar)
    │   ├── listings/page.tsx      # Ulgurji bozor & Escrow xarid modali
    │   ├── demand/page.tsx        # Teskari auksion & Fermer takliflari
    │   └── admin/page.tsx         # Admin paneli (KPI, verifikatsiya, arbitraj, CSV)
    └── package.json
```
