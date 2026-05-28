@echo off
title ARCH -- Build Windows .exe
color 0A
setlocal enabledelayedexpansion

echo.
echo  +------------------------------------------+
echo  ^|                                          ^|
echo  ^|        ARCH .exe Builder                 ^|
echo  ^|   Packages ARCH into a standalone app    ^|
echo  ^|                                          ^|
echo  +------------------------------------------+
echo.

REM ── Check Python ─────────────────────────────────────────────────────────────
echo  [1/5] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo  ERROR: Python not found!
    echo  Please install Python 3.8+ from https://www.python.org
    echo  Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)
for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo  Found Python %PYVER%

REM ── Set paths ─────────────────────────────────────────────────────────────────
set "SCRIPT_DIR=%~dp0"
set "ARCH_PY=%SCRIPT_DIR%arch.py"
set "ARCH_ICO=%SCRIPT_DIR%arch.ico"
set "ARCH_CFG=%SCRIPT_DIR%arch_config.json"
set "OUT_DIR=%SCRIPT_DIR%dist"

REM ── Find Python Scripts dir and add to PATH ───────────────────────────────────
for /f "tokens=*" %%p in ('python -c "import sysconfig; print(sysconfig.get_path(\"scripts\"))"') do set "PY_SCRIPTS=%%p"
set "PATH=%PATH%;%PY_SCRIPTS%"
echo  Python Scripts dir: %PY_SCRIPTS%

REM ── Install PyInstaller ────────────────────────────────────────────────────────
echo.
echo  [2/5] Installing build dependencies...
python -m pip install pyinstaller psutil keyboard --quiet --upgrade
if %errorlevel% neq 0 (
    echo  WARNING: pip install had issues. Continuing...
)
echo  Dependencies ready.

REM ── Patch model name ─────────────────────────────────────────────────────────
echo.
echo  [3/5] Patching source for latest Claude model...
python "%SCRIPT_DIR%patch_model.py"

REM ── Build exe ─────────────────────────────────────────────────────────────────
echo.
echo  [4/5] Building ARCH.exe (this takes 1-2 minutes)...
echo.

set "ICON_FLAG="
if exist "%ARCH_ICO%" set "ICON_FLAG=--icon "%ARCH_ICO%""

set "CFG_FLAG="
if exist "%ARCH_CFG%" set "CFG_FLAG=--add-data "%ARCH_CFG%;.""

python -m PyInstaller ^
  --onefile ^
  --windowed ^
  --name "ARCH" ^
  %ICON_FLAG% ^
  %CFG_FLAG% ^
  --hidden-import psutil ^
  --hidden-import tkinter ^
  --hidden-import tkinter.font ^
  --collect-all psutil ^
  --distpath "%OUT_DIR%" ^
  --workpath "%SCRIPT_DIR%build_tmp" ^
  --specpath "%SCRIPT_DIR%build_tmp" ^
  --noconfirm ^
  "%ARCH_PY%"

if %errorlevel% neq 0 (
    echo.
    echo  BUILD FAILED. See errors above.
    echo  Try running: python -m pip install pyinstaller --upgrade
    echo.
    pause
    exit /b 1
)

REM ── Copy config next to exe ───────────────────────────────────────────────────
echo.
echo  [5/5] Finalising output...
if exist "%ARCH_CFG%" copy /Y "%ARCH_CFG%" "%OUT_DIR%\arch_config.json" >nul
if exist "%ARCH_ICO%"  copy /Y "%ARCH_ICO%"  "%OUT_DIR%\arch.ico"  >nul

REM ── Done ──────────────────────────────────────────────────────────────────────
echo.
echo  +------------------------------------------+
echo  ^|   BUILD COMPLETE!                        ^|
echo  ^|   Your app is at: dist\ARCH.exe          ^|
echo  ^|   No Python needed on other machines!    ^|
echo  +------------------------------------------+
echo.

set /p OPEN="Open the dist folder now? (y/n): "
if /i "%OPEN%"=="y" explorer "%OUT_DIR%"

pause
