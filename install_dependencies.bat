@echo off
echo ========================================
echo Installing Dependencies for Map Location Feature
echo ========================================
echo.

echo Installing required packages...
pip install python-dotenv folium streamlit-folium requests

echo.
echo ========================================
echo Testing installation...
echo ========================================
python -c "import dotenv; import folium; import streamlit_folium; print('✅ All packages installed successfully!')"

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo You can now run: streamlit run enhanced_web_app.py
echo.
pause
