@echo off
echo ========================================
echo    MTV RESURRECTION - HOARD CONTENT
echo ========================================
echo.

echo Starting aria2c daemon...
aria2c --enable-rpc --rpc-listen-all=true --daemon=true
timeout /t 2 /nobreak >nul

echo.
echo Running main resurrection script...
python resurrect.py

echo.
echo Updating gallery...
python gallery_builder.py

echo.
echo All processes completed!
echo Visit https://expdevspace.github.io/mtv-resurrection/ to view the gallery
pause