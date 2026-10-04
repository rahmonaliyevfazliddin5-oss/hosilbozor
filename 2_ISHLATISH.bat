@echo off
chcp 65001 > nul
title HosilBozor - Tizimni Ishga Tushirish
echo ===================================================
echo     🌾 HosilBozor Ekotizimi Ishga Tushmoqda...
echo ===================================================
echo.

echo [1/3] Backend API (FastAPI) ishga tushirilmoqda...
start "HosilBozor Backend API (Port 8000)" cmd /k "cd /d %~dp0backend && if exist venv (call venv\Scripts\activate.bat) else (if exist .venv call .venv\Scripts\activate.bat) && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

timeout /t 3 /nobreak > nul

echo [2/3] Web Portal (Next.js) ishga tushirilmoqda...
start "HosilBozor Web Portal (Port 3000)" cmd /k "cd /d %~dp0web && npm run dev"

timeout /t 3 /nobreak > nul

echo [3/3] Telegram Bot (@HosilBozorBot) ishga tushirilmoqda...
start "HosilBozor Telegram Bot" cmd /k "cd /d %~dp0 && if exist backend\venv (call backend\venv\Scripts\activate.bat) else (if exist backend\.venv call backend\.venv\Scripts\activate.bat) && python run_bot.py"

echo.
echo ===================================================
echo  🚀 BARCHA XIZMATLAR ISHGA TUSHIRILDI!
echo.
echo  🌐 Web Sayt:       http://localhost:3000
echo  📚 API Hujjatlar:  http://localhost:8000/docs
echo  🤖 Telegram Bot:   @HosilBozorBot
echo ===================================================
echo.
echo Brauzerda ochish uchun istalgan tugmani bosing...
pause > nul
start http://localhost:3000
