@echo off
echo 🛑 Остановка системы "33 Зуб"...
echo.

echo 🔒 Закрытие всех окон командной строки...
taskkill /IM cmd.exe /F

echo.
echo ✅ Все сервисы остановлены
echo.
echo 💡 Для перезапуска системы используйте: start-all.bat
echo.

pause