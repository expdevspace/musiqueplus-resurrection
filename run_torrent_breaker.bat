@echo off
cls
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                                                                              ║
echo ║    ███╗   ███╗ ██████╗ ████████╗██████╗  ██████╗ ██╗   ██╗████████╗███████╗  ║
echo ║    ████╗ ████║██╔═══██╗╚══██╔══╝██╔══██╗██╔═══██╗██║   ██║╚══██╔══╝██╔════╝  ║
echo ║    ██╔████╔██║██║   ██║   ██║   ██████╔╝██║   ██║██║   ██║   ██║   █████╗    ║
echo ║    ██║╚██╔╝██║██║   ██║   ██║   ██╔══██╗██║   ██║██║   ██║   ██║   ██╔══╝    ║
echo ║    ██║ ╚═╝ ██║╚██████╔╝   ██║   ██║  ██║╚██████╔╝╚██████╔╝   ██║   ███████╗  ║
echo ║    ╚═╝     ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝   ╚══════╝  ║
echo ║                                                                              ║
echo ║              MTV RESURRECTION - TORRENT BREAKER v1.0                         ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.
echo [+] Initializing aria2c daemon...
aria2c --enable-rpc --rpc-listen-all=true --daemon=true
timeout /t 3 /nobreak >nul

echo [+] Breaking torrent veins...
python torrent_breaker.py

echo [+] Updating CRT display...
copy retro_tv_enhanced.html docs\index.html >nul

echo.
echo [+] Process completed!
echo.
echo Visit https://expdevspace.github.io/mtv-resurrection/ to view the enhanced CRT
echo.
pause