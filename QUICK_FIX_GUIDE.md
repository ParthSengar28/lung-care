# 🔧 Quick Fix Guide

## Common Installation Issues

### Issue: "ModuleNotFoundError: No module named 'dotenv'"

**Solution:**

```bash
pip install python-dotenv
```

### Issue: "ModuleNotFoundError: No module named 'folium'"

**Solution:**

```bash
pip install folium streamlit-folium
```

### Issue: Missing multiple packages

**Solution 1 - Install from requirements file:**

```bash
pip install -r requirements_enhanced.txt
```

**Solution 2 - Install individually:**

```bash
pip install python-dotenv
pip install folium
pip install streamlit-folium
pip install requests
```

**Solution 3 - Use the batch script (Windows):**

```bash
install_dependencies.bat
```

---

## Complete Installation Steps

### Step 1: Activate Virtual Environment (if using one)

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Step 2: Install All Dependencies

```bash
pip install -r requirements_enhanced.txt
```

### Step 3: Verify Installation

```bash
python -c "import dotenv; import folium; import streamlit_folium; print('✅ Success!')"
```

### Step 4: Test the Location Service

```bash
python test_location_api.py
```

### Step 5: Run the App

```bash
streamlit run enhanced_web_app.py
```

---

## Troubleshooting

### Issue: pip command not found

**Solution:** Make sure Python is installed and added to PATH

### Issue: Permission denied

**Solution:** Run command prompt as Administrator (Windows) or use `sudo` (Linux/Mac)

### Issue: Package conflicts

**Solution:**

```bash
pip install --upgrade pip
pip install -r requirements_enhanced.txt --force-reinstall
```

### Issue: Virtual environment issues

**Solution:** Create a fresh virtual environment:

```bash
# Remove old venv
rm -rf venv  # Linux/Mac
rmdir /s venv  # Windows

# Create new venv
python -m venv venv

# Activate
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install packages
pip install -r requirements_enhanced.txt
```

---

## Package Versions

If you encounter version conflicts, use these specific versions:

```
python-dotenv==1.0.0
folium==0.15.0
streamlit-folium==0.15.0
requests==2.31.0
streamlit==1.28.0
```

---

## Quick Commands Reference

```bash
# Install single package
pip install python-dotenv

# Install from requirements
pip install -r requirements_enhanced.txt

# Upgrade pip
pip install --upgrade pip

# List installed packages
pip list

# Check specific package
pip show python-dotenv

# Uninstall package
pip uninstall python-dotenv

# Install specific version
pip install python-dotenv==1.0.0
```

---

## Still Having Issues?

1. Check Python version: `python --version` (should be 3.9+)
2. Check pip version: `pip --version`
3. Try upgrading pip: `pip install --upgrade pip`
4. Check if virtual environment is activated
5. Try installing in a fresh virtual environment

---

## Success Checklist

- [ ] Virtual environment activated
- [ ] pip upgraded to latest version
- [ ] All packages from requirements_enhanced.txt installed
- [ ] Test script runs successfully: `python test_location_api.py`
- [ ] App starts without errors: `streamlit run enhanced_web_app.py`
- [ ] "Find Care" tab works in the app

---

**Need more help?** See `START_HERE.md` or `MAP_API_SETUP_GUIDE.md`
