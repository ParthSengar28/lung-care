"""
FastAPI Backend for Pneumonia Detection
RESTful API for programmatic access
"""
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import io
import os
import time
import uuid
from datetime import datetime
from typing import Optional, List
import logging
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="🫁 Pneumonia Detection API",
    description="AI-powered pneumonia detection from chest X-ray images",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for web frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API responses
class PredictionResult(BaseModel):
    prediction: str
    confidence: float
    probabilities: dict
    model_used: str
    processing_time: float
    timestamp: str
    request_id: str

class HealthCheck(BaseModel):
    status: str
    models_loaded: int
    available_models: List[str]
    timestamp: str

class PneumoniaDetectorAPI:
    def __init__(self):
        self.models = {}
        self.load_models()
        
    def load_models(self):
        """Load all available models"""
        models_dir = "models"
        model_files = {
            "hybrid": "hybrid_model_colab.h5",
            "resnet50": "resnet_classifier_colab.h5",
            "autoencoder": "autoencoder_colab.h5"
        }
        
        for model_name, model_file in model_files.items():
            model_path = os.path.join(models_dir, model_file)
            if os.path.exists(model_path):
                try:
                    self.models[model_name] = load_model(model_path)
                    logger.info(f"✅ Loaded {model_name} model")
                except Exception as e:
                    logger.error(f"❌ Failed to load {model_name}: {str(e)}")
            else:
                logger.warning(f"⚠️ Model file not found: {model_path}")
        
        logger.info(f"Loaded {len(self.models)} models: {list(self.models.keys())}")
    
    def preprocess_image(self, img_bytes: bytes) -> np.ndarray:
        """Preprocess image for model prediction"""
        try:
            # Open image
            img = Image.open(io.BytesIO(img_bytes))
            
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize to model input size
            img = img.resize((224, 224))
            
            # Convert to array and normalize
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = img_array / 255.0
            
            return img_array
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")
    
    def predict(self, img_bytes: bytes, model_name: str = "hybrid") -> PredictionResult:
        """Make prediction using specified model"""
        if model_name not in self.models:
            available_models = list(self.models.keys())
            raise HTTPException(
                status_code=400, 
                detail=f"Model '{model_name}' not available. Available models: {available_models}"
            )
        
        try:
            # Preprocess image
            img_array = self.preprocess_image(img_bytes)
            
            # Make prediction
            start_time = time.time()
            model = self.models[model_name]
            prediction = model.predict(img_array, verbose=0)
            processing_time = time.time() - start_time
            
            # Process results
            predicted_class = np.argmax(prediction[0])
            confidence = float(prediction[0][predicted_class])
            
            classes = ['NORMAL', 'PNEUMONIA']
            predicted_label = classes[predicted_class]
            
            probabilities = {
                'NORMAL': float(prediction[0][0]),
                'PNEUMONIA': float(prediction[0][1])
            }
            
            return PredictionResult(
                prediction=predicted_label,
                confidence=confidence,
                probabilities=probabilities,
                model_used=model_name,
                processing_time=processing_time,
                timestamp=datetime.now().isoformat(),
                request_id=str(uuid.uuid4())
            )
            
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

# Initialize detector
detector = PneumoniaDetectorAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    """API documentation homepage"""
    return """
    <html>
        <head>
            <title>🫁 Pneumonia Detection API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
                .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
                .header { text-align: center; color: #1f77b4; }
                .endpoint { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; }
                .method { color: #28a745; font-weight: bold; }
                .url { color: #007bff; font-family: monospace; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1 class="header">🫁 Pneumonia Detection API</h1>
                <p>AI-powered pneumonia detection from chest X-ray images</p>
                
                <h2>📋 Available Endpoints</h2>
                
                <div class="endpoint">
                    <span class="method">GET</span> <span class="url">/health</span><br>
                    Check API health and loaded models
                </div>
                
                <div class="endpoint">
                    <span class="method">POST</span> <span class="url">/predict</span><br>
                    Upload X-ray image for pneumonia detection
                </div>
                
                <div class="endpoint">
                    <span class="method">POST</span> <span class="url">/predict/{model_name}</span><br>
                    Use specific model for prediction (hybrid, resnet50, autoencoder)
                </div>
                
                <div class="endpoint">
                    <span class="method">GET</span> <span class="url">/models</span><br>
                    List all available models
                </div>
                
                <h2>📖 Documentation</h2>
                <p>
                    <a href="/docs">📚 Interactive API Documentation (Swagger)</a><br>
                    <a href="/redoc">📋 Alternative Documentation (ReDoc)</a>
                </p>
                
                <h2>🚀 Quick Start</h2>
                <pre style="background: #f1f1f1; padding: 15px; border-radius: 5px;">
# Python example
import requests

url = "http://localhost:8000/predict"
files = {"file": open("xray_image.jpg", "rb")}
response = requests.post(url, files=files)
result = response.json()
print(f"Prediction: {result['prediction']}")
                </pre>
            </div>
        </body>
    </html>
    """

@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint"""
    return HealthCheck(
        status="healthy",
        models_loaded=len(detector.models),
        available_models=list(detector.models.keys()),
        timestamp=datetime.now().isoformat()
    )

@app.get("/models")
async def list_models():
    """List all available models"""
    return {
        "available_models": list(detector.models.keys()),
        "total_models": len(detector.models),
        "recommended_model": "hybrid"
    }

@app.post("/predict", response_model=PredictionResult)
async def predict_default(file: UploadFile = File(...)):
    """Predict pneumonia using default (hybrid) model"""
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    contents = await file.read()
    return detector.predict(contents, "hybrid")

@app.post("/predict/{model_name}", response_model=PredictionResult)
async def predict_with_model(model_name: str, file: UploadFile = File(...)):
    """Predict pneumonia using specified model"""
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    contents = await file.read()
    return detector.predict(contents, model_name)

@app.post("/batch_predict")
async def batch_predict(files: List[UploadFile] = File(...), model_name: str = "hybrid"):
    """Batch prediction for multiple images"""
    if len(files) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 files allowed per batch")
    
    results = []
    for file in files:
        if not file.content_type.startswith('image/'):
            continue
        
        try:
            contents = await file.read()
            result = detector.predict(contents, model_name)
            result_dict = result.dict()
            result_dict['filename'] = file.filename
            results.append(result_dict)
        except Exception as e:
            results.append({
                'filename': file.filename,
                'error': str(e),
                'prediction': None
            })
    
    return {
        "batch_results": results,
        "total_processed": len(results),
        "model_used": model_name
    }

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Global exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)