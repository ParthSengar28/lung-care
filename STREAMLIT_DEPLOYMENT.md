# 🚀 Streamlit Cloud Deployment Guide

## ✅ Files Created for Deployment

I've created the following files to ensure smooth deployment:

1. **`requirements.txt`** - Python dependencies (Streamlit Cloud looks for this)
2. **`packages.txt`** - System-level dependencies
3. **`.streamlit/config.toml`** - Streamlit configuration

## 🔧 Pre-Deployment Checklist

### ✅ Required Files in Your GitHub Repository:

```
pneumonia-detection/
├── enhanced_web_app.py          # Main application
├── requirements.txt             # Python dependencies (REQUIRED)
├── packages.txt                 # System dependencies (REQUIRED)
├── .streamlit/
│   └── config.toml             # Streamlit config
├── README.md                    # Project description
└── .gitignore                  # Exclude models and data
```

### ❌ Files NOT to Push to GitHub:

```
# These should be in .gitignore
models/                          # Too large (100MB+ files)
data/                           # Too large (GB of images)
venv/                           # Virtual environment
__pycache__/                    # Python cache
*.h5                            # Model files
```

## 🚀 Deployment Steps

### Step 1: Prepare Your GitHub Repository

```bash
# Make sure you're in your project directory
cd D:\lung-care

# Add files to git
git add enhanced_web_app.py
git add requirements.txt
git add packages.txt
git add .streamlit/config.toml
git add README.md
git add .gitignore

# Commit
git commit -m "Add enhanced web app for Streamlit deployment"

# Push to GitHub
git push origin main
```

### Step 2: Deploy on Streamlit Cloud

1. **Go to Streamlit Cloud:**

   - Visit: https://share.streamlit.io
   - Sign in with GitHub

2. **Create New App:**

   - Click "New app"
   - Select your repository: `your-username/pneumonia-detection`
   - Branch: `main`
   - Main file path: `enhanced_web_app.py`
   - Click "Deploy"

3. **Wait for Deployment:**
   - Streamlit will install dependencies
   - This takes 3-5 minutes
   - Watch the logs for any errors

### Step 3: Configure App Settings (Optional)

In Streamlit Cloud dashboard:

- **Custom subdomain**: Choose your app URL
- **Python version**: 3.9 or 3.10
- **Secrets**: Add API keys if needed

## ⚠️ Important: Model Files Issue

### The Problem:

Your trained models (`.h5` files) are too large for GitHub (100MB limit).

### Solution Options:

#### Option 1: Use Smaller Models (Recommended for Demo)

Create a lightweight demo model or use model quantization.

#### Option 2: Host Models Externally

```python
# In enhanced_web_app.py, add model download function
import requests
import os

def download_model_if_needed():
    """Download model from external source"""
    model_url = "https://your-storage-url/hybrid_model_colab.h5"
    model_path = "models/hybrid_model_colab.h5"

    if not os.path.exists(model_path):
        os.makedirs("models", exist_ok=True)
        print("Downloading model...")
        response = requests.get(model_url)
        with open(model_path, 'wb') as f:
            f.write(response.content)
        print("Model downloaded!")

# Call this before loading models
download_model_if_needed()
```

#### Option 3: Use Google Drive

```python
import gdown

def download_from_gdrive():
    """Download model from Google Drive"""
    # Share your model file on Google Drive and get the file ID
    file_id = "your-google-drive-file-id"
    output = "models/hybrid_model_colab.h5"

    if not os.path.exists(output):
        os.makedirs("models", exist_ok=True)
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, output, quiet=False)

# Add gdown to requirements.txt
# gdown==4.7.1
```

#### Option 4: Use Hugging Face Hub

```python
from huggingface_hub import hf_hub_download

def download_from_huggingface():
    """Download model from Hugging Face"""
    model_path = hf_hub_download(
        repo_id="your-username/pneumonia-detection",
        filename="hybrid_model_colab.h5",
        cache_dir="models"
    )
    return model_path

# Add to requirements.txt
# huggingface-hub==0.19.0
```

## 🔧 Troubleshooting Common Errors

### Error 1: "ModuleNotFoundError: No module named 'plotly'"

**Solution:** Ensure `requirements.txt` exists and contains all dependencies.

### Error 2: "No module named 'cv2'"

**Solution:** Use `opencv-python-headless` instead of `opencv-python` in requirements.txt.

### Error 3: "Model file not found"

**Solution:** Implement one of the model hosting solutions above.

### Error 4: "Memory limit exceeded"

**Solution:**

- Use `tensorflow-cpu` instead of `tensorflow`
- Reduce model size
- Optimize image processing

### Error 5: "Build failed"

**Solution:** Check the build logs in Streamlit Cloud dashboard for specific errors.

## 📝 Quick Fix for Current Deployment

Since you're getting the plotly error, here's what to do:

### Immediate Fix:

1. **Ensure `requirements.txt` is in your repository root:**

   ```bash
   git add requirements.txt
   git commit -m "Add requirements.txt for Streamlit deployment"
   git push origin main
   ```

2. **Redeploy on Streamlit Cloud:**

   - Go to your app dashboard
   - Click "Reboot app" or "Redeploy"
   - Wait for installation to complete

3. **Check Build Logs:**
   - Watch the logs during deployment
   - Look for "Successfully installed" messages
   - Verify all packages are installed

## 🎯 Recommended Deployment Strategy

### For Demo/Presentation (Without Models):

Create a demo version that doesn't require actual models:

```python
# demo_web_app.py
import streamlit as st

st.title("🫁 Pneumonia Detection Demo")
st.info("This is a demo version. Upload functionality coming soon!")

# Show sample results
if st.button("Show Sample Analysis"):
    st.success("Sample Result: NORMAL")
    st.write("Confidence: 92.5%")

    # Show all other features (videos, hospitals, treatment info)
    # These don't require models
```

### For Full Deployment (With Models):

1. Upload models to Google Drive
2. Add download function to app
3. Deploy to Streamlit Cloud
4. Models download on first run

## 🌟 Alternative: Deploy Without Models

You can deploy the interface and features without AI detection:

```python
# In enhanced_web_app.py, modify load_models():

def load_models(self):
    """Load models or use demo mode"""
    models_dir = "models"

    # Check if models exist
    if not os.path.exists(models_dir):
        st.sidebar.warning("⚠️ Running in DEMO mode (models not loaded)")
        self.demo_mode = True
        return

    # Try to load models
    # ... existing code
```

## 📊 Deployment Checklist

- [ ] `requirements.txt` in repository root
- [ ] `packages.txt` in repository root
- [ ] `.streamlit/config.toml` configured
- [ ] `.gitignore` excludes large files
- [ ] Models hosted externally (if needed)
- [ ] Code pushed to GitHub
- [ ] App deployed on Streamlit Cloud
- [ ] Build logs checked for errors
- [ ] App tested and working

## 🎉 Success!

Once deployed, your app will be available at:

```
https://your-app-name.streamlit.app
```

Share this URL with anyone to showcase your project! 🚀

## 💡 Pro Tips

1. **Use Streamlit Secrets** for API keys
2. **Monitor app usage** in Streamlit Cloud dashboard
3. **Update app** by pushing to GitHub (auto-deploys)
4. **Check logs** regularly for errors
5. **Optimize performance** by caching data

Your enhanced pneumonia detection app is now ready for the world! 🌍
