@echo off
cls
echo ========================================
echo Clinical Workflow Automation Agent UI
echo ========================================
echo.
echo Starting Streamlit server...
echo.
echo The UI will be available at:
echo    http://localhost:8501
echo.
echo Your browser should open automatically.
echo If not, please open the URL above manually.
echo.
echo Press Ctrl+C to stop the server when done.
echo.
echo ========================================
echo.

python -m streamlit run app.py

