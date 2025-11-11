# 🚀 Streamlit Cloud Deployment Guide

## Quick Deploy Steps

### 1. Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Pneumonia Detection App"

# Create GitHub repo and push
# Go to github.com and create a new repository named "pneumonia-detection"
# Then run:
git remote add origin https://github.com/YOUR_USERNAME/pneumonia-detection.git
git branch -M main
git push -u origin main
```

### 2. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository: `YOUR_USERNAME/pneumonia-detection`
5. Set main file path: `enhanced_web_app.py`
6. Click "Deploy"

### 3. Important Notes

⚠️ **Model Files**: Your trained models (`.h5` files) are too large for GitHub (>100MB). The app will run in "demo mode" without models on Streamlit Cloud.

**Options:**

- **Option A (Recommended)**: Use the app to showcase UI/UX features without actual AI predictions
- **Option B**: Host models on Google Drive and download them at runtime (see below)
- **Option C**: Use a smaller model or quantized version

### Option B: Download Models from Google Drive

If you want full functionality, upload your models to Google Drive and modify the app:

1. Upload `models/hybrid_model_colab.h5` to Google Drive
2. Make it publicly accessible
3. Get the file ID from the share link
4. Add this code to `enhanced_web_app.py`:

```python
import gdown

def download_models():
    """Download models from Google Drive"""
    model_url = "https://drive.google.com/uc?id=YOUR_FILE_ID"
    output = "models/hybrid_model_colab.h5"

    if not os.path.exists(output):
        os.makedirs("models", exist_ok=True)
        gdown.download(model_url, output, quiet=False)
```

Add `gdown` to requirements.txt:

```
gdown==4.7.1
```

## 🎯 What Works on Streamlit Cloud

✅ Beautiful UI and interface
✅ Image upload and preprocessing
✅ YouTube video recommendations
✅ Treatment information
✅ Hospital locator map
✅ All visualizations and charts

❌ AI predictions (without models)

## 🔗 After Deployment

Your app will be available at:

```
https://YOUR_USERNAME-pneumonia-detection-enhanced-web-app-xxxxx.streamlit.app
```

Share this link with anyone!

## 📝 Tips

- First deployment takes 5-10 minutes
- App will auto-update when you push to GitHub
- Check logs in Streamlit Cloud dashboard for errors
- Free tier has resource limits (1GB RAM, 1 CPU)

## 🆘 Troubleshooting

**Build fails?**

- Check requirements.txt for version conflicts
- Ensure all imports are available
- Check Streamlit Cloud logs

**App crashes?**

- Reduce memory usage
- Optimize image processing
- Use smaller models

**Models not loading?**

- Expected if models not in repo
- App will show error message
- Use Google Drive option above
