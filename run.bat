@echo off
echo Generating dashboard for Tilak Varma...

python create_dashboard.py "Tilak Varma" > output.log 2>&1

if %errorlevel% equ 0 (
    echo.
    echo Success! The dashboard has been generated.
    echo You can now open 'dashboard.html'.
) else (
    echo.
    echo An error occurred. Please ensure Python is installed and the required libraries (pandas, plotly) are installed as per README.txt.
)

pause
