# 🚀 Deployment Guide - Pneumonia Detection System

Complete guide to deploy your pneumonia detection system for public use.

## 🎯 Deployment Options

### Option 1: Quick Local Deployment (Recommended for Testing)

```bash
# Install web dependencies
pip install -r requirements_web.txt

# Start web application
python deploy.py --mode web
```

**Access at:** http://localhost:8501

### Option 2: API Server Deployment

```bash
# Start API server
python deploy.py --mode api
```

**Access at:**

- API: http://localhost:8000
- Documentation: http://localhost:8000/docs

### Option 3: Full Stack Deployment

```bash
# Start both web app and API
python deploy.py --mode both
```

**Access at:**

- Web App: http://localhost:8501
- API: http://localhost:8000

### Option 4: Docker Deployment (Production Ready)

```bash
# Deploy with Docker
python deploy.py --mode docker
```

**Access at:**

- Web App: http://localhost:8501
- API: http://localhost:8000

## 🌐 Cloud Deployment Options

### Streamlit Cloud (Easiest)

1. **Push to GitHub:**

   ```bash
   git add .
   git commit -m "Add pneumonia detection app"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud:**

   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select `web_app.py` as main file
   - Deploy!

3. **Your app will be live at:** `https://your-app-name.streamlit.app`

### Heroku Deployment

```bash
# Prepare for Heroku
python deploy.py --mode heroku

# Deploy to Heroku (requires Heroku CLI)
heroku login
heroku create your-pneumonia-app
git push heroku main
heroku ps:scale web=1
```

### Railway Deployment

1. **Connect GitHub to Railway:**

   - Go to [railway.app](https://railway.app)
   - Connect your GitHub repository
   - Select deployment branch

2. **Configure:**
   - Set start command: `streamlit run web_app.py --server.port=$PORT`
   - Add environment variables if needed

### Google Cloud Run

```bash
# Build and deploy to Cloud Run
gcloud run deploy pneumonia-detection \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## 📱 Mobile-Friendly Features

Your web app includes:

- ✅ Responsive design for mobile devices
- ✅ Touch-friendly interface
- ✅ Image upload from camera or gallery
- ✅ Progressive Web App (PWA) capabilities

## 🔒 Security Considerations

### For Production Deployment:

1. **Add Authentication:**

   ```python
   # Add to web_app.py
   import streamlit_authenticator as stauth

   # Configure authentication
   authenticator = stauth.Authenticate(...)
   name, authentication_status, username = authenticator.login('Login', 'main')
   ```

2. **Rate Limiting:**

   ```python
   # Add to api_server.py
   from slowapi import Limiter

   limiter = Limiter(key_func=get_remote_address)
   app.state.limiter = limiter

   @app.post("/predict")
   @limiter.limit("10/minute")
   async def predict(...):
   ```

3. **HTTPS Configuration:**
   - Use SSL certificates
   - Configure reverse proxy (Nginx)
   - Enable CORS properly

## 📊 Monitoring & Analytics

### Add Usage Analytics:

```python
# Add to web_app.py
import streamlit.components.v1 as components

# Google Analytics
components.html("""
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
""")
```

### Health Monitoring:

```python
# Add to api_server.py
@app.get("/metrics")
async def metrics():
    return {
        "predictions_count": prediction_counter,
        "uptime": time.time() - start_time,
        "memory_usage": psutil.virtual_memory().percent
    }
```

## 🎨 Customization Options

### Branding:

1. **Update Colors:**

   ```python
   # In web_app.py, modify CSS
   st.markdown("""
   <style>
   .main-header { color: #your-brand-color; }
   </style>
   """, unsafe_allow_html=True)
   ```

2. **Add Logo:**

   ```python
   # Add to web_app.py
   st.image("your-logo.png", width=200)
   ```

3. **Custom Domain:**
   - Configure DNS settings
   - Set up SSL certificate
   - Update deployment configuration

## 📈 Performance Optimization

### Model Optimization:

```python
# Convert to TensorFlow Lite for faster inference
import tensorflow as tf

converter = tf.lite.TFLiteConverter.from_saved_model("models/hybrid_model_colab.h5")
tflite_model = converter.convert()

# Save optimized model
with open("models/hybrid_model_optimized.tflite", "wb") as f:
    f.write(tflite_model)
```

### Caching:

```python
# Add to web_app.py
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("models/hybrid_model_colab.h5")
```

## 🔧 Troubleshooting

### Common Issues:

1. **Models not loading:**

   ```bash
   # Check models directory
   ls -la models/

   # Verify file permissions
   chmod 644 models/*.h5
   ```

2. **Memory issues:**

   ```python
   # Reduce model size or use model quantization
   # Add memory cleanup
   import gc
   gc.collect()
   ```

3. **Slow predictions:**
   ```python
   # Use TensorFlow Lite
   # Implement model caching
   # Optimize image preprocessing
   ```

## 📋 Deployment Checklist

### Pre-Deployment:

- [ ] Models trained and saved
- [ ] Dependencies installed
- [ ] Local testing completed
- [ ] Security measures implemented
- [ ] Performance optimized

### Post-Deployment:

- [ ] Health checks configured
- [ ] Monitoring set up
- [ ] Backup strategy in place
- [ ] Documentation updated
- [ ] User feedback system

## 🎉 Success Metrics

Your deployment is successful when:

- ✅ Web app loads in <3 seconds
- ✅ Predictions complete in <2 seconds
- ✅ 99%+ uptime
- ✅ Mobile-friendly interface
- ✅ Secure HTTPS connection

## 🆘 Support & Maintenance

### Regular Maintenance:

1. **Update dependencies monthly**
2. **Monitor performance metrics**
3. **Backup models and data**
4. **Review security logs**
5. **Update documentation**

### Getting Help:

- Check logs for error messages
- Test with sample images
- Verify model file integrity
- Review deployment configuration

## 🌟 Advanced Features

### Future Enhancements:

1. **Multi-language support**
2. **Batch processing interface**
3. **Medical report generation**
4. **Integration with PACS systems**
5. **Real-time collaboration tools**

Your pneumonia detection system is now ready for production deployment! 🚀
