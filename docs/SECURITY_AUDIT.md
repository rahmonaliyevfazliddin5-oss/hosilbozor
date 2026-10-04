# HosilBozor Xavfsizlik Auditi va Himoya Standartlari (Security Audit & OWASP Top 10)

Ushbu hujjat **HosilBozor** agrar web-platformasining xavfsizlik arxitekturasi, OWASP Top 10 standartlariga muvofiqligi va audit xulosasini taqdim etadi.

---

## 1. OWASP Top 10 Baholash Jadvali

| Xavf (OWASP 2021) | HosilBozor Himoya Mexanizmi | Holat |
| :--- | :--- | :--- |
| **A01: Broken Access Control** | Qat'iy RBAC (Fermer, Xaridor, Haydovchi, Admin). Resurs egaligini tekshirish (o'z e'lonini faqat egasi o'zgartira oladi). Barcha admin yo'llari `require_role([UserRole.ADMIN])` bilan himoyalangan. | ✅ **Himoyalangan** |
| **A02: Cryptographic Failures** | Parollar `bcrypt` (salt rounds) bilan shifrlanadi. JWT tokenlar HS256 / RS256 orqali imzolanadi. Karta ma'lumotlari platformada HECH QACHON saqlanmaydi (Escrow port/adapter arxitekturasi). | ✅ **Himoyalangan** |
| **A03: Injection (SQLi, Command)** | SQLAlchemy 2.0 ORM parametrli so'rovlari (Prepared Statements) ishlatiladi. Xom SQL (raw queries) mavjud emas. PostGIS koordinatalari float tipida qat'iy tekshiriladi. | ✅ **Himoyalangan** |
| **A04: Insecure Design** | Buyurtma holati chekli avtomat (Finite State Machine) orqali boshqariladi. Ruxsat berilmagan o'tishlar qat'iyan rad etiladi. To'lov chiqishi faqat topshirish kodi va xaridor tasdig'idan so'ng amalga oshadi. | ✅ **Himoyalangan** |
| **A05: Security Misconfiguration** | CORS sozlamalari ruxsat etilgan domenlar bilan cheklangan. `.env` orqali sirlar boshqariladi. Kod bazasida API kalitlar yoki tokenlar qattiq kodlanmagan (`.env.example`). | ✅ **Himoyalangan** |
| **A06: Vulnerable & Outdated Components** | Barcha Python va Node kutubxonalari zamonaviy versiyalarda (`fastapi>=0.115`, `pydantic>=2.7`, `next>=14.2.5`, `aiogram>=3.10`). | ✅ **Himoyalangan** |
| **A07: Identification & Auth Failures** | Qisqa muddatli Access Token (30 min) va Refresh Token rotatsiyasi. OTP generatsiyasi kriptografik `secrets` moduli orqali amalga oshiriladi (rate limiting mavjud). | ✅ **Himoyalangan** |
| **A08: Software & Data Integrity Failures** | Payme va Click webhooklari tranzaksiya imzosi va parolini tekshiradi. Idempotent webhook qayta ishlash — bitta to'lov ikki marta hisobga olinmaydi. | ✅ **Himoyalangan** |
| **A09: Security Logging & Monitoring** | Barcha kritik buyurtma holatlari, to'lovlar va admin qarorlari o'zgarmas `OrderEvent` va `AuditLog` jurnallariga yozib boriladi. | ✅ **Himoyalangan** |
| **A10: SSRF & Insecure File Upload** | Rasmlar mijoz tomonida siqilib (HTML5 WebP), fayl hajmi va MIME-turi serverda tekshiriladi. UUID asosida xavfsiz fayl nomlari generatsiya qilinadi (Path traversal himoyasi). | ✅ **Himoyalangan** |

---

## 2. To'lov va Escrow Xavfsizligi

1. **Zero Card Storage (Karta ma'lumotlarini saqlamaslik):**
   - HosilBozor foydalanuvchilarning bank karta raqamlari yoki CVV kodlariga kirish huquqiga ega emas.
   - Barcha to'lovlar Payme, Click yoki Uzum to'lov shlyuzlari orqali amalga oshiriladi.
2. **Escrow Izolyatsiyasi:**
   - Xaridor to'lagan mablag' platformaning maxsus tranzit hisobida (escrow ledger) muzlatiladi (`HOLD`).
   - Mablag' faqat quyidagi 2 ta shart bajarilgandagina fermer va haydovchiga o'tkaziladi:
     1. Haydovchi yukni fermerdan olganida fermer bergan 6 xonali **Qabul Kodi**ni kiritishi;
     2. Xaridorga yetkazilganda xaridor taqdim etgan 6 xonali **Topshirish Kodi** kiritilishi va buyurtma `COMPLETED` bo'lishi.
3. **Nizo va Muzlatish (Dispute Freeze):**
   - Agar xaridor yoki sotuvchi nizo ochsa, buyurtma holati `DISPUTED`ga o'tadi va barcha to'lovlar avtomatik bloklanadi.
   - Nizo faqat Admin/Arbitraj tekshiruvidan keyingina xaridorga qaytariladi (`refund_to_buyer`) yoki sotuvchiga chiqariladi (`release_to_seller`).

---

## 3. Shaxsiy Ma'lumotlarni Himoyalash (PII Minimization)

- Fermer va haydovchilarning pasport va shaxsiy ma'lumotlari faqat tasdiqlash jarayoni uchun admin ko'rishiga ruxsat etilgan.
- Ochiq API javoblarida faqat zaruriy maydonlar (Ism, xo'jalik nomi, reyting, mashina turi) qaytariladi; shaxsiy telefon va telegram ID xavfsiz saqlanadi.
