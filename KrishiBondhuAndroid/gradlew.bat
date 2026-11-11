@echo off
setlocal EnableExtensions
set "ROOT=%~dp0"
set "VERSION=8.11.1"
set "DIST=%USERPROFILE%\.gradle\nexus-wrapper\gradle-%VERSION%"
set "ZIP=%USERPROFILE%\.gradle\nexus-wrapper\gradle-%VERSION%-bin.zip"
if not exist "%DIST%\bin\gradle.bat" (
  if not exist "%USERPROFILE%\.gradle\nexus-wrapper" mkdir "%USERPROFILE%\.gradle\nexus-wrapper"
  echo Downloading Gradle %VERSION% on first run. This may take a few minutes...
  powershell -NoProfile -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri 'https://services.gradle.org/distributions/gradle-%VERSION%-bin.zip' -OutFile '%ZIP%'"
  if errorlevel 1 (echo Gradle download failed. Check internet connection. & exit /b 1)
  powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -LiteralPath '%ZIP%' -DestinationPath '%USERPROFILE%\.gradle\nexus-wrapper' -Force"
  if errorlevel 1 (echo Gradle extraction failed. & exit /b 1)
)
call "%DIST%\bin\gradle.bat" -p "%ROOT%" %*
exit /b %ERRORLEVEL%
