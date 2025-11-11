"""
Advanced Pneumonia Detection Web Interface
Modern Streamlit app with multiple features
"""
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image, ImageEnhance
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os
import time
import io
import base64
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Configure page
st.set_page_config(
    page_title="🫁 Pneumonia Detection AI",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-box {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .normal-prediction {
        background-color: #d4edda;
        border: 2px solid #28a745;
    }
    .pneumonia-prediction {
        background-color: #f8d7da;
        border: 2px solid #dc3545;
    }
    .confidence-high {
        color: #28a745;
        font-weight: bold;
    }
    .confidence-medium {
        color: #ffc107;
        font-weight: bold;
    }
    .confidence-low {
        color: #dc3545;
        font-weight: bold;
    }
    .stButton > button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

class PneumoniaDetectorApp:
    def __init__(self):
        self.models = {}
        self.load_models()
        
    def load_models(self):
        """Load all available models"""
        models_dir = "models"
        model_files = {
            "Hybrid Model (Best)": "hybrid_model_colab.h5",
            "ResNet50 Classifier": "resnet_classifier_colab.h5",
            "Autoencoder": "autoencoder_colab.h5"
        }
        
        for model_name, model_file in model_files.items():
            model_path = os.path.join(models_dir, model_file)
            if os.path.exists(model_path):
                try:
                    self.models[model_name] = load_model(model_path)
                    st.sidebar.success(f"✅ {model_name} loaded")
                except Exception as e:
                    st.sidebar.error(f"❌ Failed to load {model_name}: {str(e)}")
            else:
                st.sidebar.warning(f"⚠️ {model_name} not found")
    
    def preprocess_image(self, img, target_size=(224, 224)):
        """Preprocess image for model prediction"""
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        img_resized = img.resize(target_size)
        img_array = image.img_to_array(img_resized)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0
        
        return img_array
    
    def predict(self, img, model_name):
        """Make prediction using selected model"""
        if model_name not in self.models:
            return None
        
        model = self.models[model_name]
        img_array = self.preprocess_image(img)
        
        start_time = time.time()
        prediction = model.predict(img_array, verbose=0)
        inference_time = time.time() - start_time
        
        predicted_class = np.argmax(prediction[0])
        confidence = prediction[0][predicted_class]
        
        classes = ['NORMAL', 'PNEUMONIA']
        predicted_label = classes[predicted_class]
        
        return {
            'prediction': predicted_label,
            'confidence': float(confidence),
            'probabilities': {
                'NORMAL': float(prediction[0][0]),
                'PNEUMONIA': float(prediction[0][1])
            },
            'inference_time': inference_time
        }
    
    def enhance_image(self, img, brightness=1.0, contrast=1.0, sharpness=1.0):
        """Apply image enhancements"""
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(brightness)
        
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(contrast)
        
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(sharpness)
        
        return img
    
    def create_confidence_chart(self, probabilities):
        """Create confidence visualization"""
        fig = go.Figure(data=[
            go.Bar(
                x=list(probabilities.keys()),
                y=list(probabilities.values()),
                marker_color=['#28a745' if k == 'NORMAL' else '#dc3545' for k in probabilities.keys()],
                text=[f"{v:.1%}" for v in probabilities.values()],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="Prediction Confidence",
            yaxis_title="Probability",
            xaxis_title="Class",
            showlegend=False,
            height=400
        )
        
        return fig
    
    def get_confidence_color(self, confidence):
        """Get color class based on confidence level"""
        if confidence >= 0.9:
            return "confidence-high"
        elif confidence >= 0.7:
            return "confidence-medium"
        else:
            return "confidence-low"

def main():
    # Initialize app
    app = PneumoniaDetectorApp()
    
    # Header
    st.markdown('<h1 class="main-header">AI-Powered Pneumonia Detection</h1>', unsafe_allow_html=True)
    st.markdown("### Upload a chest X-ray image to detect pneumonia using advanced AI models")
    
    # Sidebar
    st.sidebar.title("Settings")
    
    # Model selection
    if app.models:
        selected_model = st.sidebar.selectbox(
            "Select AI Model",
            list(app.models.keys()),
            help="Choose which AI model to use for prediction"
        )
    else:
        st.error("No models found! Please ensure your trained models are in the 'models' directory.")
        st.stop()
    
    # Image enhancement controls
    st.sidebar.subheader("Image Enhancement")
    brightness = st.sidebar.slider("Brightness", 0.5, 2.0, 1.0, 0.1)
    contrast = st.sidebar.slider("Contrast", 0.5, 2.0, 1.0, 0.1)
    sharpness = st.sidebar.slider("Sharpness", 0.5, 2.0, 1.0, 0.1)
    
    # Advanced options
    st.sidebar.subheader("Advanced Options")
    show_probabilities = st.sidebar.checkbox("Show detailed probabilities", True)
    show_processing_time = st.sidebar.checkbox("Show processing time", True)
    save_results = st.sidebar.checkbox("Save results to history", False)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📤 Upload X-ray Image")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choose a chest X-ray image",
            type=['jpg', 'jpeg', 'png', 'bmp', 'tiff'],
            help="Upload a clear chest X-ray image for analysis"
        )
        
        # Sample images
        st.subheader("Or Try Sample Images")
        sample_col1, sample_col2 = st.columns(2)
        
        with sample_col1:
            if st.button("Load Normal Sample"):
                # You can add sample images here
                st.info("Add sample normal X-ray to your project")
        
        with sample_col2:
            if st.button("Load Pneumonia Sample"):
                # You can add sample images here
                st.info("Add sample pneumonia X-ray to your project")
    
    with col2:
        st.subheader("Analysis Results")
        
        if uploaded_file is not None:
            # Load and display image
            img = Image.open(uploaded_file)
            
            # Apply enhancements
            enhanced_img = app.enhance_image(img, brightness, contrast, sharpness)
            
            # Display original and enhanced images
            img_col1, img_col2 = st.columns(2)
            
            with img_col1:
                st.write("**Original Image**")
                st.image(img, use_column_width=True)
            
            with img_col2:
                st.write("**Enhanced Image**")
                st.image(enhanced_img, use_column_width=True)
            
            # Prediction button
            if st.button("Analyze X-ray", key="predict_btn"):
                with st.spinner("Analyzing image..."):
                    # Make prediction
                    result = app.predict(enhanced_img, selected_model)
                    
                    if result:
                        # Display results
                        prediction = result['prediction']
                        confidence = result['confidence']
                        
                        # Main prediction box
                        box_class = "normal-prediction" if prediction == "NORMAL" else "pneumonia-prediction"
                        confidence_class = app.get_confidence_color(confidence)
                        
                        st.markdown(f"""
                        <div class="prediction-box {box_class}">
                            <h2>Prediction: {prediction}</h2>
                            <h3 class="{confidence_class}">Confidence: {confidence:.1%}</h3>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Detailed results
                        if show_probabilities:
                            st.subheader(" Detailed Analysis")
                            
                            # Confidence chart
                            fig = app.create_confidence_chart(result['probabilities'])
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Probability table
                            prob_df = pd.DataFrame([
                                {"Class": "Normal", "Probability": f"{result['probabilities']['NORMAL']:.2%}"},
                                {"Class": "Pneumonia", "Probability": f"{result['probabilities']['PNEUMONIA']:.2%}"}
                            ])
                            st.table(prob_df)
                        
                        # Processing info
                        if show_processing_time:
                            st.info(f" Processing time: {result['inference_time']:.3f} seconds")
                        
                        # Medical disclaimer
                        st.warning("""
                         **Medical Disclaimer**: This AI tool is for educational and research purposes only. 
                        It should not be used as a substitute for professional medical diagnosis. 
                        Always consult with qualified healthcare professionals for medical decisions.
                        """)
                        
                        # Save results
                        if save_results:
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            result_data = {
                                'timestamp': timestamp,
                                'model': selected_model,
                                'prediction': prediction,
                                'confidence': confidence,
                                'filename': uploaded_file.name
                            }
                            
                            # Save to session state for history
                            if 'prediction_history' not in st.session_state:
                                st.session_state.prediction_history = []
                            st.session_state.prediction_history.append(result_data)
                            
                            st.success(" Results saved to history!")
    
    # History section
    if save_results and 'prediction_history' in st.session_state and st.session_state.prediction_history:
        st.subheader(" Prediction History")
        
        history_df = pd.DataFrame(st.session_state.prediction_history)
        st.dataframe(history_df, use_container_width=True)
        
        # Download history
        csv = history_df.to_csv(index=False)
        st.download_button(
            label="📥 Download History as CSV",
            data=csv,
            file_name=f"pneumonia_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p> Pneumonia Detection AI | Built with Streamlit & TensorFlow</p>
        <p>Trained on chest X-ray dataset using ResNet50 + Autoencoder hybrid architecture</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()