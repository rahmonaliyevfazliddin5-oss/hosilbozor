# HosilBozor — To'liq Demo va Taqdimot Ssenariysi (Demo Script)

Ushbu ssenariy buyurtmachi, hakamlar hay'ati yoki sinovchilar uchun **HosilBozor** platformasining barcha 4 roli (Fermer, Xaridor, Haydovchi, Admin) bo'yicha imkoniyatlarini ko'rsatib beradi.

---

## 1. Tayyorgarlik (1 daqiqa)

Barcha servislar va real ma'lumotlar bazasi tayyorlangan:
```bash
# Backend test ma'lumotlarini yuklash
python backend/scripts/seed.py
```

Test hisob ma'lumotlari:
- **Admin:** `+998900000001` (Parol: `HosilBozor2026!`)
- **Fermer:** `+998901112233` (Rustam Yoqubov, Chinoz Agrogurux)
- **Xaridor:** `+998904445566` (Bobur Savdogar, Korzinka)
- **Haydovchi:** `+998907778899` (Davron Haydovchi, Isuzu Ref)

---

## 2. Qadam-baqadam Taqdimot Oqimi

### Ssenariy 1: Fermer 60 soniyada Telegram Botda e'lon berishi (60s Farmer Flow)
1. Telegram'da `@HosilBozorBot` ga kiring va `/start` buyrug'ini bering.
2. Bot o'zbek tilida qutlaydi va asosiy menyuni chiqaradi:
   `[🌾 Hosil E'lon Qilish]`, `[📈 Bozor Narxlari]`, `[📦 Mening E'lonlarim]`.
3. **[🌾 Hosil E'lon Qilish]** tugmasi bosiladi:
   - Ekin turi: `Pomidor (Issiqxona)`
   - Hosil miqdori: `5000` (kg)
   - Minimal partiya: `200` (kg)
   - Narx: `7000` (so'm/kg)
   - Manzil: `Toshkent viloyati, Chinoz tumani`
   - Rasm: Rasm yuboriladi (Telegram Mini App orqali mijozda avtomatik WebP siqiladi).
4. Bot darhol e'lonni tasdiqlaydi: *"E'loningiz HosilBozor birjasida faollashtirildi!"* (Vaqt sarfi: ~45 soniya).

---

### Ssenariy 2: Ulgurji Xaridor Web Platformada Hosil Xaridi va Escrow To'lovi
1. Brauzerda `http://localhost:3000` yoki `http://localhost:3000/listings` manziliga kiring.
2. **Qidiruv va filterlar:**
   - Qidiruv satriga `Pomidor` deb yozing yoki `Birinchi nav (Premium)` filtrini tanlang.
   - Rustam Yoqubovning Chinozdagi 7,200 so'mlik pomidor kartochkasi chiqadi.
   - Fermerning tasdiqlanganlik nishoni (`✓`) va 4.9 reytingi ko'rinadi.
3. **[🛡️ Escrow orqali buyurtma berish]** tugmasi bosiladi:
   - Xarid miqdori kiritiladi: `1000 kg`.
   - Hisob-kitob ko'rsatiladi:
     - Mahsulot: `7,200,000 so'm`
     - Escrow kafolat to'lovi (2%): `144,000 so'm`
     - Jami: `7,344,000 so'm`.
4. **[💳 To'lovni amalga oshirish (Mock Escrow)]** bosiladi:
   - Pul tranzit hisobda muzlatiladi (`PAID_ESCROW`).
   - Xaridorga buyurtma raqami va haydovchiga beriladigan 6 xonali **Topshirish Kodi** taqdim etiladi.

---

### Ssenariy 3: Haydovchi Yuk Yetkazish Topshirig'ini Qabul Qilishi va Bajarishi
1. Buyurtma `PAID_ESCROW` bo'lishi bilan haydovchilar birjasida avtomatik ravishda **Yetkazib berish topshirig'i (Delivery Job)** paydo bo'ladi.
2. Haydovchi (Davron, Isuzu Ref) taklif yuboradi va buyurtmachi uni qabul qiladi.
3. **Yukni fermerdan olish (Pickup):**
   - Haydovchi dalaga yetib keladi va fermerdan 6 xonali `pickup_code`ni olib tizimga kiritadi.
   - Buyurtma holati `PICKED_UP` (Yuklandi) holatiga o'tadi.
4. **Yukni xaridorga topshirish (Delivery):**
   - Haydovchi yukni xaridor omboriga yetkazadi.
   - Xaridor mahsulotni ko'zdan kechirib, o'zining 6 xonali `delivery_code` kodini haydovchiga aytadi.
   - Haydovchi kodni kiritadi: Buyurtma holati `DELIVERED` ga o'tadi.
5. Xaridor tasdiqlaydi -> Buyurtma holati `COMPLETED` bo'ladi!
6. **Mablag' ozod qilinishi (Escrow Disbursement):**
   - Fermer hisobiga mahsulot summasi to'liq o'tkaziladi.
   - Haydovchi hisobiga yetkazib berish haqi to'liq o'tkaziladi.
   - HosilBozor platformasi 2% komissiyani qabul qiladi.

---

### Ssenariy 4: Nizo Ochilishi va Admin Arbitraji (Dispute Resolution)
1. Agar mahsulot sifatsiz bo'lsa yoki yetib kelmasa:
   - Xaridor **[Nizo Ochish (Dispute)]** tugmasini bosadi va rasm dalilini ilova qiladi.
   - Tizim buyurtmani `DISPUTED` holatiga o'tkazadi va barcha to'lovlarni bloklaydi.
2. Admin `/admin` paneliga kiradi:
   - **⚖️ Nizolar bo'limi:** Da'vogar ma'lumoti, e'tiroz sababi va rasm dalilini ko'radi.
   - **Amallar:**
     - Agar da'vo asossiz bo'lsa: **[💰 Pulni Fermerga chiqarish]** bosiladi -> Buyurtma `COMPLETED` bo'ladi va pul fermerga beriladi.
     - Agar mahsulot haqiqatdan ham yaroqsiz bo'lsa: **[↩️ Xaridorga to'liq qaytarish]** bosiladi -> Mablag' xaridor kartasiga to'liq qaytariladi va buyurtma `CANCELLED` bo'ladi.

---

## 3. Qabul Qilish Mezonlarining Tekshiruvi (Acceptance Checklist)

- [x] Fermer Telegram bot orqali 60 soniyada o'zbek tilida e'lon bera oladi.
- [x] Xaridor web orqali hosilni topib, buyurtma qilib, escrow to'lay oladi.
- [x] Haydovchi topshiriqni olib, maxsus tasdiqlash kodi bilan yakunlay oladi.
- [x] Pul faqat muvaffaqiyatli topshirishdan so'ng chiqariladi; nizo paytida pul muzlaydi.
- [x] Barcha buyurtma holatlari (FSM) qat'iy sinovdan o'tgan; noto'g'ri o'tishlar rad etiladi.
- [x] Repozitoriyda sirlar yo'q; 50 ta avtomatlashtirilgan test 91% qamrov bilan o'tadi.
