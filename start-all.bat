@echo off
echo 🚀 Запуск системы "33 Зуб"...
echo.

REM Проверка наличия Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python не найден. Установите Python 3.9+ и добавьте в PATH.
    pause
    exit /b 1
)

REM Проверка наличия Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js не найден. Установите Node.js 16+ и добавьте в PATH.
    pause
    exit /b 1
)

REM Проверка наличия npm
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm не найден. Убедитесь, что Node.js установлен правильно.
    pause
    exit /b 1
)

echo ✅ Проверка окружения завершена
echo.

REM Запуск backend сервера
echo 📡 Запуск backend сервера...
start "Backend Server" cmd /k "cd backend && python main.py"

REM Установка и запуск frontend
echo 🌐 Установка зависимостей frontend...
cd frontend
npm install
if %errorlevel% neq 0 (
    echo ❌ Ошибка установки зависимостей frontend
    pause
    exit /b 1
)

echo 🚀 Запуск frontend...
start "Frontend" cmd /k "npm run dev"

REM Установка и запуск admin
echo 🔒 Установка зависимостей admin...
cd ../admin
npm install
if %errorlevel% neq 0 (
    echo ❌ Ошибка установки зависимостей admin
    pause
    exit /b 1
)

echo 🚀 Запуск admin панели...
start "Admin Panel" cmd /k "npm run dev"

echo.
echo 📋 СЕРВИСЫ ЗАПУЩЕНЫ:
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:5173
echo   Admin:    http://localhost:3001
echo.
echo 📖 Для тестирования системы запустите: python test-setup.py
echo.
echo ⚠️  Для остановки всех сервисов закройте все окна командной строки
echo.

pause