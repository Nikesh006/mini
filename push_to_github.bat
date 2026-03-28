@echo off
if not exist .git (
    git init
)
git add .
git commit -m "Prepare to deploy gymcopy to TiDB and Render"
git branch -M main
git remote remove origin 2>nul
git remote add origin https://github.com/Nikesh006/mini.git
echo Pushing code to GitHub... (This may open a prompt for GitHub credentials)
git push -u origin main
if %ERRORLEVEL% neq 0 (
    echo.
    echo -------------------------------------------------------------------
    echo FAILED to push to GitHub. 
    echo Please make sure you are authenticated with GitHub, and the repository https://github.com/Nikesh006/mini.git exists and you have write access.
    echo -------------------------------------------------------------------
) else (
    echo.
    echo -------------------------------------------------------------------
    echo Successfully pushed code to https://github.com/Nikesh006/mini.git!
    echo You can now go to Render.com and select this repository to deploy.
    echo -------------------------------------------------------------------
)
