# 📦 Google Drive Model Setup Guide

## Why Google Drive?

Your trained model files (`.h5`) are too large for GitHub (>100MB limit). We'll host them on Google Drive and download them automatically when the app starts on Streamlit Cloud.

## Step-by-Step Setup

### 1. Upload Models to Google Drive

1. Go to [Google Drive](https://drive.google.com)
2. Create a new folder called `pneumonia-models` (optional, for organization)
3. Upload your model files:
   - `hybrid_model_colab.h5`
   - `resnet_classifier_colab.h5`

### 2. Make Models Publicly Accessible

For each model file:

1. **Right-click** on the file → **Share**
2. Click **"Change to anyone with the link"**
3. Set permission to **"Viewer"**
4. Click **"Copy link"**

You'll get a link like:

```
https://drive.google.com/file/d/1ABC123xyz_YOUR_FILE_ID_HERE/view?usp=sharing
```

### 3. Extract File IDs

From the link above, extract the FILE_ID (the part between `/d/` and `/view`):

```
1ABC123xyz_YOUR_FILE_ID_HERE
```

### 4. Update the Code

Open `enhanced_web_app.py` and find this section (around line 118):

```python
self.model_urls = {
    "Hybrid Model (Best)": "YOUR_GOOGLE_DRIVE_FILE_ID_HERE",
    "ResNet50 Classifier": "YOUR_GOOGLE_DRIVE_FILE_ID_HERE_2"
}
```

Replace with your actual file IDs:

```python
self.model_urls = {
    "Hybrid Model (Best)": "1ABC123xyz_YOUR_ACTUAL_FILE_ID",
    "ResNet50 Classifier": "1XYZ789abc_YOUR_ACTUAL_FILE_ID_2"
}
```

### 5. Push to GitHub

```bash
git add enhanced_web_app.py
git commit -m "Add Google Drive model URLs"
git push
```

### 6. Deploy!

Streamlit Cloud will automatically:

1. Detect the push
2. Rebuild the app
3. Download models from Google Drive on first run
4. Cache them for future use

## ⚡ Performance Notes

- **First load**: Takes 2-3 minutes (downloading models)
- **Subsequent loads**: Instant (models are cached)
- **Model size**: Each model is ~80-100MB

## 🔒 Security

- Models are read-only (Viewer permission)
- No authentication required
- Anyone with the link can download (but that's okay for a public demo)

## 🆘 Troubleshooting

**"Failed to download model"**

- Check if the file is publicly accessible
- Verify the file ID is correct
- Make sure the file hasn't been deleted

**"Model loading error"**

- Ensure the model file is a valid `.h5` file
- Check if TensorFlow version is compatible
- Try re-uploading the model

**"Out of memory"**

- Streamlit Cloud free tier has 1GB RAM
- Both models together might be too large
- Consider using only one model

## 💡 Alternative: Use One Model Only

If you hit memory limits, use only the best model:

```python
self.model_urls = {
    "Hybrid Model (Best)": "1ABC123xyz_YOUR_FILE_ID",
}

model_files = {
    "Hybrid Model (Best)": "hybrid_model_colab.h5",
}
```

## ✅ Verification

After deployment, check the Streamlit Cloud logs:

- You should see "📥 Downloading..." messages
- Then "✅ Model loaded" messages
- If successful, the app will work with full AI predictions!

---

**Need help?** Check the Streamlit Cloud logs for detailed error messages.
