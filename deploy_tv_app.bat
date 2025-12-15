@echo off
cls
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                                                                              ║
echo ║    ██████╗ ███████╗██████╗ ██╗      █████╗ ██╗   ██╗████████╗███████╗        ║
echo ║    ██╔══██╗██╔════╝██╔══██╗██║     ██╔══██╗██║   ██║╚══██╔══╝██╔════╝        ║
echo ║    ██║  ██║█████╗  ██████╔╝██║     ███████║██║   ██║   ██║   █████╗          ║
echo ║    ██║  ██║██╔══╝  ██╔═══╝ ██║     ██╔══██║██║   ██║   ██║   ██╔══╝          ║
echo ║    ██████╔╝███████╗██║     ███████╗██║  ██║╚██████╔╝   ██║   ███████╗        ║
echo ║    ╚═════╝ ╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝        ║
echo ║                                                                              ║
echo ║              RETRO TV APP - DEPLOY TO GITHUB PAGES                          ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.
echo [+] Building TV app for production...
cd tv-app
npm run build
cd ..

echo.
echo [+] Adding built files to git...
git add docs/

echo.
echo [+] Committing changes...
git commit -m "Deploy TV app to GitHub Pages"

echo.
echo [+] Pushing to GitHub...
git push origin main

echo.
echo [+] Deployment complete!
echo    Visit: https://expdevspace.github.io/musiqueplus-resurrection/
echo.
pause