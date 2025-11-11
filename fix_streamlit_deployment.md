# 🔧 Quick Fix for Streamlit Deployment Error

## Your Current Error:

```
File "/mount/src/pneumonia-detection/enhanced_web_app.py", line 18, in <module>
    import plotly.graph_objects as go
ModuleNotFoundError: No module named 'plotly'
```

## ✅ Solution: 3 Simple Steps

### Step 1: Ensure `requirements.txt` is in Your Repository

```bash
# Check if requirements.txt exists
ls requirements.txt

# If it exists, check its content
cat requirements.txt
```

### Step 2: Push `requirements.txt` to GitHub

```bash
# Add the file
git add requirements.txt
git add packages.txt
git add .streamlit/config.toml

# Commit
git commit -m "Fix: Add requirements.txt for Streamlit Cloud deployment"

# Push to GitHub
git push origin main
```

### Step 3: Redeploy on Streamlit Cloud

1. Go to https://share.streamlit.io
2. Find your app in the dashboard
3. Click the **"⋮"** menu (three dots)
4. Select **"Reboot app"**
5. Wait 3-5 minutes for redeployment

## 🎯 What Should Happen:

Streamlit Cloud will:

1. ✅ Find `requirements.txt` in your repository
2. ✅ Install all packages (including plotly)
3. ✅ Install system dependencies from `packages.txt`
4. ✅ Start your app successfully

## 📋 Verify Your Files:

Your repository should have these files:

```
pneumonia-detection/
├── enhanced_web_app.py          ✅ Main app
├── requirements.txt             ✅ MUST HAVE
├── packages.txt                 ✅ MUST HAVE
├── .streamlit/
│   └── config.toml             ✅ Optional but recommended
└── .gitignore                  ✅ Exclude large files
```

## ⚠️ Common Mistakes:

### Mistake 1: Wrong filename

- ❌ `requirements_enhanced.txt`
- ✅ `requirements.txt` (Streamlit looks for this exact name)

### Mistake 2: File not in repository root

- ❌ `src/requirements.txt`
- ✅ `requirements.txt` (must be in root directory)

### Mistake 3: File not pushed to GitHub

```bash
# Make sure you pushed it
git status  # Should show "nothing to commit"
```

## 🚀 Alternative: Quick Deploy Command

If you're starting fresh:

```bash
# Navigate to your project
cd D:\lung-care

# Create/verify requirements.txt exists
cat requirements.txt

# Add and push all necessary files
git add requirements.txt packages.txt .streamlit/config.toml enhanced_web_app.py
git commit -m "Add deployment files for Streamlit Cloud"
git push origin main

# Now redeploy on Streamlit Cloud
```

## 🔍 Check Deployment Logs:

On Streamlit Cloud:

1. Go to your app dashboard
2. Click on your app
3. Look at the **"Manage app"** section
4. Check **"Logs"** tab
5. You should see:
   ```
   Successfully installed plotly-5.17.0
   Successfully installed streamlit-1.28.0
   Successfully installed folium-0.15.0
   ...
   ```

## ✅ Success Indicators:

You'll know it worked when you see:

- ✅ "Your app is live!" message
- ✅ No red error messages
- ✅ App loads at your Streamlit URL
- ✅ All features work (except model loading if models not uploaded)

## 💡 If Still Not Working:

### Check 1: Verify requirements.txt content

```bash
cat requirements.txt
```

Should contain:

```
tensorflow-cpu==2.13.0
streamlit==1.28.0
plotly==5.17.0
folium==0.15.0
streamlit-folium==0.15.0
...
```

### Check 2: Verify file is on GitHub

Go to: `https://github.com/your-username/pneumonia-detection/blob/main/requirements.txt`

Should show the file content.

### Check 3: Clear Streamlit Cache

In Streamlit Cloud:

- Settings → Advanced → Clear cache
- Reboot app

## 🎉 Once Fixed:

Your app will be live at:

```
https://your-app-name.streamlit.app
```

The plotly error will be gone, and all visualizations will work! 🚀
