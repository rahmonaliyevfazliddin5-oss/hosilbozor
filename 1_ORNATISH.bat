@echo off
chcp 65001 > nul
title HosilBozor - O'rnatish (Setup)
echo ===================================================
echo     🌾 HosilBozor Loyihasini O'rnatish
echo ===================================================
echo.

echo [1/3] Python virtual muhitini sozlash (backend)...
cd backend
if not exist venv (
    echo Virtual muhit (venv) yaratilmoqda...
    python -m venv venv
)
call venv\Scripts\activate.bat
echo Backend kutubxonalari o'rnatilmoqda...
python -m pip install --upgrade pip
pip install -r requirements.txt
cd ..

echo.
echo [2/3] Web kutubxonalari o'rnatilmoqda (Next.js frontend)...
cd web
call npm install
cd ..

echo.
echo [3/3] Konfiguratsiya fayllarini tekshirish...
if not exist .env (
    copy .env.example .env
    echo .env fayli yaratildi.
)

echo.
echo ===================================================
echo  ✅ O'RNATISH MUVAFFAQIYATLI YAKUNLANDI!
echo  Endi "2_ISHLATISH.bat" faylini ishga tushiring.
echo ===================================================
pause
