@echo off
echo Exporting gym database...
mysqldump -u root -p"Nikesh@2006" gym > gym_dump.sql
if %ERRORLEVEL% neq 0 (
    echo Failed to dump database.
    exit /b %ERRORLEVEL%
)

echo Creating gymcopy database...
mysql -u root -p"Nikesh@2006" -e "CREATE DATABASE IF NOT EXISTS gymcopy;"
if %ERRORLEVEL% neq 0 (
    echo Failed to create database.
    exit /b %ERRORLEVEL%
)

echo Importing into gymcopy database...
mysql -u root -p"Nikesh@2006" gymcopy < gym_dump.sql
if %ERRORLEVEL% neq 0 (
    echo Failed to import database.
    exit /b %ERRORLEVEL%
)

echo Database clone completed successfully!
