@echo off
cls
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                                                                              ║
echo ║    ██████╗ ██╗ █████╗ ██╗      ██████╗ ██████╗ ██╗   ██╗███████╗██████╗      ║
echo ║    ██╔══██╗██║██╔══██╗██║     ██╔════╝██╔═══██╗██║   ██║██╔════╝██╔══██╗     ║
echo ║    ██║  ██║██║███████║██║     ██║     ██║   ██║██║   ██║█████╗  ██████╔╝     ║
echo ║    ██║  ██║██║██╔══██║██║     ██║     ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗     ║
echo ║    ██████╔╝██║██║  ██║███████╗╚██████╗╚██████╔╝ ╚████╔╝ ███████╗██║  ██║     ║
echo ║    ╚═════╝ ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝     ║
echo ║                                                                              ║
echo ║              RETRO TV APP - DIAGNOSTIC TOOL                                  ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.
echo [+] How it works ^& Your Privacy:
echo     This diagnostic tool analyzes your local TV app installation.
echo     No data is sent to any external servers. All analysis is done locally.
echo     Session data is automatically deleted when you close this tool.
echo.
echo [1] Quick Health Check
echo [2] Smart Cleanup (Remove build artifacts and reinstall dependencies)
echo [3] Nuclear Reset (Complete reset to fresh installation)
echo [4] Guided Setup (Step-by-step installation guide)
echo [5] Exit
echo.
choice /c 12345 /m "Select an option"
if errorlevel 5 goto :exit
if errorlevel 4 goto :guided_setup
if errorlevel 3 goto :nuclear_reset
if errorlevel 2 goto :smart_cleanup
if errorlevel 1 goto :quick_check

:quick_check
echo.
echo [+] Performing quick health check...
echo    Checking Node.js installation...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo    ❌ Node.js not found. Please install Node.js from https://nodejs.org/
    goto :menu
)
echo    ✅ Node.js is installed

echo    Checking npm installation...
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo    ❌ npm not found. Please install Node.js which includes npm
    goto :menu
)
echo    ✅ npm is installed

echo    Checking TV app dependencies...
cd tv-app >nul 2>&1
if exist node_modules (
    echo    ✅ Dependencies are installed
) else (
    echo    ⚠️  Dependencies not installed. Run 'npm install' to install them
)
cd .. >nul 2>&1

echo    Checking build files...
if exist docs\index.html (
    echo    ✅ Build files exist
) else (
    echo    ⚠️  Build files missing. Run 'npm run build' to generate them
)
echo.
echo [+] Health check complete!
goto :menu

:smart_cleanup
echo.
echo [+] Performing smart cleanup...
echo    Removing build artifacts...
rd /s /q docs\assets >nul 2>&1
del /q docs\index.html >nul 2>&1
echo    ✅ Build artifacts removed

echo    Removing node_modules...
cd tv-app >nul 2>&1
rd /s /q node_modules >nul 2>&1
echo    ✅ node_modules removed

echo    Reinstalling dependencies...
npm install
if %errorlevel% neq 0 (
    echo    ❌ Failed to install dependencies
    goto :menu
)
echo    ✅ Dependencies reinstalled

echo    Rebuilding app...
npm run build
if %errorlevel% neq 0 (
    echo    ❌ Failed to build app
    goto :menu
)
echo    ✅ App rebuilt successfully
cd .. >nul 2>&1
echo.
echo [+] Smart cleanup complete!
goto :menu

:nuclear_reset
echo.
echo [⚠️ ] WARNING: This will completely reset your TV app installation!
echo    All customizations and downloaded content will be lost.
echo.
choice /m "Are you sure you want to proceed with nuclear reset"
if errorlevel 2 goto :menu

echo.
echo [+] Performing nuclear reset...
echo    Removing all TV app files...
rd /s /q tv-app >nul 2>&1
rd /s /q docs >nul 2>&1
echo    ✅ TV app files removed

echo    Restoring from git...
git checkout -- tv-app docs
if %errorlevel% neq 0 (
    echo    ❌ Failed to restore from git
    goto :menu
)
echo    ✅ Files restored from git

echo    Installing dependencies...
cd tv-app
npm install
if %errorlevel% neq 0 (
    echo    ❌ Failed to install dependencies
    goto :menu
)
echo    ✅ Dependencies installed

echo    Building app...
npm run build
if %errorlevel% neq 0 (
    echo    ❌ Failed to build app
    goto :menu
)
echo    ✅ App built successfully
cd ..
echo.
echo [+] Nuclear reset complete!
goto :menu

:guided_setup
echo.
echo [+] Guided Setup
echo    Step 1: Checking prerequisites...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo    ❌ Node.js not found. Please install Node.js from https://nodejs.org/
    echo    Press any key to continue...
    pause >nul
    goto :menu
)
echo    ✅ Node.js is installed

npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo    ❌ npm not found. Please install Node.js which includes npm
    echo    Press any key to continue...
    pause >nul
    goto :menu
)
echo    ✅ npm is installed

echo    Step 2: Installing dependencies...
cd tv-app
if exist node_modules (
    echo    ⚠️  Dependencies already installed. Skipping...
) else (
    npm install
    if %errorlevel% neq 0 (
        echo    ❌ Failed to install dependencies
        echo    Press any key to continue...
        pause >nul
        goto :menu
    )
    echo    ✅ Dependencies installed
)

echo    Step 3: Building the app...
if exist ../docs/index.html (
    echo    ⚠️  App already built. Skipping...
) else (
    npm run build
    if %errorlevel% neq 0 (
        echo    ❌ Failed to build app
        echo    Press any key to continue...
        pause >nul
        goto :menu
    )
    echo    ✅ App built successfully
)
cd ..
echo.
echo [+] Guided setup complete!
echo    You can now run 'serve_tv_app.bat' to test the app locally
echo    Or run 'deploy_tv_app.bat' to deploy to GitHub Pages
echo.
echo    Press any key to continue...
pause >nul
goto :menu

:menu
echo.
echo [+] Returning to main menu...
timeout /t 2 /nobreak >nul
goto :start

:exit
echo.
echo [+] Thank you for using the TV App Diagnostic Tool!
echo    All session data has been automatically deleted.
echo.
echo    Press any key to exit...
pause >nul
exit /b

:start
cls
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                                                                              ║
echo ║    ██████╗ ██╗ █████╗ ██╗      ██████╗ ██████╗ ██╗   ██╗███████╗██████╗      ║
echo ║    ██╔══██╗██║██╔══██╗██║     ██╔════╝██╔═══██╗██║   ██║██╔════╝██╔══██╗     ║
echo ║    ██║  ██║██║███████║██║     ██║     ██║   ██║██║   ██║█████╗  ██████╔╝     ║
echo ║    ██║  ██║██║██╔══██║██║     ██║     ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗     ║
echo ║    ██████╔╝██║██║  ██║███████╗╚██████╗╚██████╔╝ ╚████╔╝ ███████╗██║  ██║     ║
echo ║    ╚═════╝ ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝     ║
echo ║                                                                              ║
echo ║              RETRO TV APP - DIAGNOSTIC TOOL                                  ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.
echo [+] How it works ^& Your Privacy:
echo     This diagnostic tool analyzes your local TV app installation.
echo     No data is sent to any external servers. All analysis is done locally.
echo     Session data is automatically deleted when you close this tool.
echo.
echo [1] Quick Health Check
echo [2] Smart Cleanup (Remove build artifacts and reinstall dependencies)
echo [3] Nuclear Reset (Complete reset to fresh installation)
echo [4] Guided Setup (Step-by-step installation guide)
echo [5] Exit
echo.
choice /c 12345 /m "Select an option"
if errorlevel 5 goto :exit
if errorlevel 4 goto :guided_setup
if errorlevel 3 goto :nuclear_reset
if errorlevel 2 goto :smart_cleanup
if errorlevel 1 goto :quick_check