@echo off
echo ========================================
echo    MTV RESURRECTION - RUN SCRIPTS
echo ========================================
echo.

echo Starting aria2c daemon...
aria2c --enable-rpc --rpc-listen-all=true --daemon=true
timeout /t 2 /nobreak >nul

echo.
echo Running English torrent search...
python torrent_en.py

echo.
echo Running French torrent search...
python torrent_fr.py

echo.
echo Updating gallery...
python gallery_builder.py

echo.
echo All processes completed!
echo Visit https://expdevspace.github.io/mtv-resurrection/ to view the gallery
pause