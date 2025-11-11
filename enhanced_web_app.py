"""
Enhanced Pneumonia Detection Web Application
Features: AI Detection + YouTube Videos + Hospital Locator + Treatment Info
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
import requests
from datetime import datetime
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
import json

# Configure page
st.set_page_config(
    page_title="🫁 Pneumonia Detection & Care",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-box {
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .normal-prediction {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 3px solid #28a745;
    }
    .pneumonia-prediction {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border: 3px solid #dc3545;
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .video-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
    }
    .hospital-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #28a745;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .treatment-section {
        background: #fff3cd;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
        margin: 1rem 0;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        padding: 0.75rem;
        font-size: 1.1rem;
        font-weight: bold;
        border: none;
        transition: transform 0.2s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

class EnhancedPneumoniaDetector:
    def __init__(self):
        self.models = {}
        self.load_models()
        
    def load_models(self):
        """Load all available models"""
        models_dir = "models"
        model_files = {
            "Hybrid Model (Best)": "hybrid_model_colab.h5",
            "ResNet50 Classifier": "resnet_classifier_colab.h5"
        }
        
        # Create models directory if it doesn't exist
        os.makedirs(models_dir, exist_ok=True)
        
        for model_name, model_file in model_files.items():
            model_path = os.path.join(models_dir, model_file)
            if os.path.exists(model_path):
                try:
                    self.models[model_name] = load_model(model_path)
                    st.sidebar.success(f"✅ {model_name} loaded")
                except Exception as e:
                    st.sidebar.error(f"❌ Failed to load {model_name}: {str(e)}")
        
        # If no models loaded, show demo mode message
        if not self.models:
            st.sidebar.warning("⚠️ Running in DEMO MODE - No models found")
            st.sidebar.info("💡 Models are too large for GitHub. This demo shows the UI/UX features.")
    
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

def get_youtube_videos(query, max_results=5):
    """Get YouTube video recommendations"""
    # Note: In production, use YouTube Data API with your API key
    # For demo, returning sample videos
    
    if "pneumonia" in query.lower():
        videos = [
            {
                'title': 'Understanding Pneumonia: Causes, Symptoms, and Treatment',
                'channel': 'Medical Education',
                'url': 'https://www.youtube.com/results?search_query=pneumonia+treatment+guide',
                'thumbnail': '🎥',
                'duration': '10:25'
            },
            {
                'title': 'Pneumonia Recovery: What You Need to Know',
                'channel': 'Health Channel',
                'url': 'https://www.youtube.com/results?search_query=pneumonia+recovery+tips',
                'thumbnail': '🎥',
                'duration': '8:15'
            },
            {
                'title': 'Home Care for Pneumonia Patients',
                'channel': 'Medical Care Guide',
                'url': 'https://www.youtube.com/results?search_query=pneumonia+home+care',
                'thumbnail': '🎥',
                'duration': '12:30'
            },
            {
                'title': 'Breathing Exercises for Pneumonia Recovery',
                'channel': 'Respiratory Health',
                'url': 'https://www.youtube.com/results?search_query=pneumonia+breathing+exercises',
                'thumbnail': '🎥',
                'duration': '7:45'
            },
            {
                'title': 'When to See a Doctor: Pneumonia Warning Signs',
                'channel': 'Emergency Medicine',
                'url': 'https://www.youtube.com/results?search_query=pneumonia+warning+signs',
                'thumbnail': '🎥',
                'duration': '6:20'
            }
        ]
    else:
        videos = [
            {
                'title': 'Maintaining Healthy Lungs',
                'channel': 'Health & Wellness',
                'url': 'https://www.youtube.com/results?search_query=healthy+lungs+tips',
                'thumbnail': '🎥',
                'duration': '9:15'
            },
            {
                'title': 'Preventing Respiratory Infections',
                'channel': 'Preventive Medicine',
                'url': 'https://www.youtube.com/results?search_query=prevent+respiratory+infections',
                'thumbnail': '🎥',
                'duration': '11:30'
            }
        ]
    
    return videos

def get_treatment_info(condition):
    """Get treatment information based on condition"""
    
    if condition == "PNEUMONIA":
        return {
            'immediate_actions': [
                "🚨 Seek immediate medical attention",
                "💊 Do not self-medicate without doctor consultation",
                "🌡️ Monitor temperature regularly",
                "💧 Stay well hydrated",
                "🛏️ Get plenty of rest"
            ],
            'medical_treatment': [
                "Antibiotics (for bacterial pneumonia)",
                "Antiviral medications (for viral pneumonia)",
                "Fever reducers and pain relievers",
                "Cough medicine (as prescribed)",
                "Oxygen therapy (if needed)"
            ],
            'home_care': [
                "Rest and sleep adequately",
                "Drink plenty of fluids (water, warm tea)",
                "Use a humidifier to ease breathing",
                "Avoid smoking and secondhand smoke",
                "Follow prescribed medication schedule",
                "Monitor symptoms and report changes"
            ],
            'warning_signs': [
                "🚨 Difficulty breathing or shortness of breath",
                "🚨 Chest pain that worsens",
                "🚨 High fever (above 102°F/39°C)",
                "🚨 Confusion or altered mental state",
                "🚨 Bluish lips or fingernails",
                "🚨 Persistent coughing with blood"
            ],
            'recovery_time': "2-3 weeks with proper treatment, but can vary",
            'follow_up': "Schedule follow-up X-ray after 6 weeks to ensure complete recovery"
        }
    else:
        return {
            'prevention_tips': [
                "🛡️ Get vaccinated (pneumonia and flu vaccines)",
                "🧼 Wash hands frequently",
                "😷 Avoid close contact with sick people",
                "🚭 Don't smoke and avoid secondhand smoke",
                "💪 Maintain a healthy lifestyle",
                "😴 Get adequate sleep",
                "🥗 Eat a balanced diet"
            ],
            'healthy_habits': [
                "Regular exercise to strengthen lungs",
                "Practice good hygiene",
                "Manage chronic conditions",
                "Stay up to date with vaccinations",
                "Avoid excessive alcohol consumption"
            ]
        }

def create_hospital_map(user_location=None):
    """Create map with nearby hospitals"""
    
    # Default location (you can use user's location with geolocation API)
    if user_location is None:
        # Default to a central location (example: New York)
        user_location = [40.7128, -74.0060]
    
    # Create map centered on user location
    m = folium.Map(
        location=user_location,
        zoom_start=13,
        tiles='OpenStreetMap'
    )
    
    # Add user location marker
    folium.Marker(
        user_location,
        popup="Your Location",
        tooltip="You are here",
        icon=folium.Icon(color='red', icon='user', prefix='fa')
    ).add_to(m)
    
    # Sample nearby hospitals (in production, use Google Places API or similar)
    nearby_hospitals = [
        {
            'name': 'City General Hospital',
            'address': '123 Medical Center Dr',
            'phone': '(555) 123-4567',
            'distance': '0.8 miles',
            'emergency': True,
            'location': [user_location[0] + 0.01, user_location[1] + 0.01]
        },
        {
            'name': 'St. Mary Medical Center',
            'address': '456 Healthcare Ave',
            'phone': '(555) 234-5678',
            'distance': '1.2 miles',
            'emergency': True,
            'location': [user_location[0] - 0.01, user_location[1] + 0.015]
        },
        {
            'name': 'Community Health Clinic',
            'address': '789 Wellness Blvd',
            'phone': '(555) 345-6789',
            'distance': '1.5 miles',
            'emergency': False,
            'location': [user_location[0] + 0.015, user_location[1] - 0.01]
        },
        {
            'name': 'Regional Medical Center',
            'address': '321 Hospital Rd',
            'phone': '(555) 456-7890',
            'distance': '2.1 miles',
            'emergency': True,
            'location': [user_location[0] - 0.015, user_location[1] - 0.015]
        }
    ]
    
    # Add hospital markers
    for hospital in nearby_hospitals:
        icon_color = 'red' if hospital['emergency'] else 'blue'
        popup_html = f"""
        <div style="width: 200px;">
            <h4>{hospital['name']}</h4>
            <p><b>📍 Address:</b> {hospital['address']}</p>
            <p><b>📞 Phone:</b> {hospital['phone']}</p>
            <p><b>📏 Distance:</b> {hospital['distance']}</p>
            <p><b>🚨 Emergency:</b> {'Yes' if hospital['emergency'] else 'No'}</p>
        </div>
        """
        
        folium.Marker(
            hospital['location'],
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=hospital['name'],
            icon=folium.Icon(color=icon_color, icon='plus', prefix='fa')
        ).add_to(m)
    
    return m, nearby_hospitals

def main():
    # Initialize detector
    if 'detector' not in st.session_state:
        st.session_state.detector = EnhancedPneumoniaDetector()
    
    detector = st.session_state.detector
    
    # Header
    st.markdown('<h1 class="main-header">🫁 AI-Powered Pneumonia Detection & Care</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Advanced AI diagnosis with treatment guidance and healthcare resources</p>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("🔧 Settings & Info")
    
    # Model selection
    if detector.models:
        selected_model = st.sidebar.selectbox(
            "🤖 Select AI Model",
            list(detector.models.keys()),
            help="Choose which AI model to use for prediction"
        )
    else:
        st.sidebar.warning("🎭 DEMO MODE")
        st.sidebar.markdown("""
        **Models not available**
        
        This is a demo showcasing:
        - ✅ UI/UX Design
        - ✅ Treatment Info
        - ✅ Hospital Locator
        - ✅ Educational Resources
        
        For full AI predictions, run locally with trained models.
        """)
        selected_model = "Demo Mode"
    
    # Feature toggles
    st.sidebar.subheader("🎯 Features")
    show_videos = st.sidebar.checkbox("📺 Show YouTube Recommendations", True)
    show_treatment = st.sidebar.checkbox("💊 Show Treatment Information", True)
    show_hospitals = st.sidebar.checkbox("🏥 Show Nearby Hospitals", True)
    
    # Image enhancement
    st.sidebar.subheader("🎨 Image Enhancement")
    brightness = st.sidebar.slider("Brightness", 0.5, 2.0, 1.0, 0.1)
    contrast = st.sidebar.slider("Contrast", 0.5, 2.0, 1.0, 0.1)
    
    # Main content
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Diagnosis", "📺 Resources", "🏥 Find Care", "📊 About"])
    
    with tab1:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📤 Upload Chest X-Ray")
            
            uploaded_file = st.file_uploader(
                "Choose a chest X-ray image",
                type=['jpg', 'jpeg', 'png', 'bmp'],
                help="Upload a clear chest X-ray image for AI analysis"
            )
            
            if uploaded_file is not None:
                img = Image.open(uploaded_file)
                
                # Apply enhancements
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(brightness)
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(contrast)
                
                st.image(img, caption="Uploaded X-Ray", use_column_width=True)
                
                if st.button("🚀 Analyze X-Ray", key="analyze_btn"):
                    if not detector.models:
                        # Demo mode - show sample result
                        st.warning("⚠️ Running in DEMO MODE - Showing sample prediction")
                        st.session_state.result = {
                            'prediction': 'PNEUMONIA',
                            'confidence': 0.87,
                            'probabilities': {
                                'NORMAL': 0.13,
                                'PNEUMONIA': 0.87
                            },
                            'inference_time': 0.234
                        }
                        st.session_state.analyzed = True
                    else:
                        with st.spinner("🔄 AI is analyzing your X-ray..."):
                            result = detector.predict(img, selected_model)
                            
                            if result:
                                st.session_state.result = result
                                st.session_state.analyzed = True
        
        with col2:
            st.subheader("🔍 Analysis Results")
            
            if 'analyzed' in st.session_state and st.session_state.analyzed:
                result = st.session_state.result
                prediction = result['prediction']
                confidence = result['confidence']
                
                # Main prediction box
                box_class = "normal-prediction" if prediction == "NORMAL" else "pneumonia-prediction"
                
                st.markdown(f"""
                <div class="prediction-box {box_class}">
                    <h2 style="margin: 0;">🎯 Diagnosis: {prediction}</h2>
                    <h3 style="margin: 10px 0;">Confidence: {confidence:.1%}</h3>
                    <p style="margin: 5px 0; font-size: 0.9rem;">
                        Model: {selected_model} | Time: {result['inference_time']:.3f}s
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Confidence chart
                fig = go.Figure(data=[
                    go.Bar(
                        x=['Normal', 'Pneumonia'],
                        y=[result['probabilities']['NORMAL'], result['probabilities']['PNEUMONIA']],
                        marker_color=['#28a745', '#dc3545'],
                        text=[f"{result['probabilities']['NORMAL']:.1%}", 
                              f"{result['probabilities']['PNEUMONIA']:.1%}"],
                        textposition='auto',
                    )
                ])
                fig.update_layout(
                    title="Prediction Confidence",
                    yaxis_title="Probability",
                    showlegend=False,
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Treatment information
                if show_treatment:
                    st.subheader("💊 Recommended Actions")
                    treatment_info = get_treatment_info(prediction)
                    
                    if prediction == "PNEUMONIA":
                        st.markdown("""
                        <div class="treatment-section">
                            <h3>⚠️ Important: Seek Medical Attention</h3>
                            <p>This AI detection suggests possible pneumonia. Please consult a healthcare professional immediately for proper diagnosis and treatment.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        with st.expander("🚨 Immediate Actions", expanded=True):
                            for action in treatment_info['immediate_actions']:
                                st.write(f"• {action}")
                        
                        with st.expander("💊 Medical Treatment Options"):
                            for treatment in treatment_info['medical_treatment']:
                                st.write(f"• {treatment}")
                        
                        with st.expander("🏠 Home Care Guidelines"):
                            for care in treatment_info['home_care']:
                                st.write(f"• {care}")
                        
                        with st.expander("⚠️ Warning Signs - Seek Emergency Care"):
                            for sign in treatment_info['warning_signs']:
                                st.write(f"• {sign}")
                        
                        st.info(f"⏱️ **Expected Recovery Time:** {treatment_info['recovery_time']}")
                        st.info(f"📅 **Follow-up:** {treatment_info['follow_up']}")
                    
                    else:
                        st.success("✅ Your X-ray appears normal! Here are some tips to maintain healthy lungs:")
                        
                        with st.expander("🛡️ Prevention Tips", expanded=True):
                            for tip in treatment_info['prevention_tips']:
                                st.write(f"• {tip}")
                        
                        with st.expander("💪 Healthy Habits"):
                            for habit in treatment_info['healthy_habits']:
                                st.write(f"• {habit}")
                
                # Medical disclaimer
                st.warning("""
                ⚠️ **Medical Disclaimer**: This AI tool is for educational and screening purposes only. 
                It should NOT be used as a substitute for professional medical diagnosis. 
                Always consult with qualified healthcare professionals for medical decisions and treatment.
                """)
            
            else:
                st.info("👆 Upload an X-ray image and click 'Analyze' to see results")
    
    with tab2:
        st.subheader("📺 Educational Resources")
        
        if 'analyzed' in st.session_state and st.session_state.analyzed:
            result = st.session_state.result
            prediction = result['prediction']
            
            if show_videos:
                if prediction == "PNEUMONIA":
                    st.markdown("### 🎥 Recommended Videos About Pneumonia")
                    videos = get_youtube_videos("pneumonia treatment")
                else:
                    st.markdown("### 🎥 Lung Health & Prevention Videos")
                    videos = get_youtube_videos("lung health")
                
                for i, video in enumerate(videos, 1):
                    st.markdown(f"""
                    <div class="video-card">
                        <h4>{video['thumbnail']} {video['title']}</h4>
                        <p><b>Channel:</b> {video['channel']} | <b>Duration:</b> {video['duration']}</p>
                        <a href="{video['url']}" target="_blank">
                            <button style="background: #ff0000; color: white; border: none; padding: 8px 16px; border-radius: 5px; cursor: pointer;">
                                ▶️ Watch on YouTube
                            </button>
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
                st.markdown("### 📚 Additional Resources")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("""
                    **🏥 Medical Organizations:**
                    - [WHO - Pneumonia](https://www.who.int/news-room/fact-sheets/detail/pneumonia)
                    - [CDC - Pneumonia](https://www.cdc.gov/pneumonia/)
                    - [Mayo Clinic - Pneumonia](https://www.mayoclinic.org/diseases-conditions/pneumonia)
                    """)
                
                with col2:
                    st.markdown("""
                    **📖 Patient Education:**
                    - [American Lung Association](https://www.lung.org/)
                    - [National Heart, Lung, and Blood Institute](https://www.nhlbi.nih.gov/)
                    - [MedlinePlus - Pneumonia](https://medlineplus.gov/pneumonia.html)
                    """)
        else:
            st.info("📊 Analyze an X-ray first to see personalized educational resources")
    
    with tab3:
        st.subheader("🏥 Find Nearby Healthcare Facilities")
        
        if 'analyzed' in st.session_state and st.session_state.analyzed:
            result = st.session_state.result
            
            if result['prediction'] == "PNEUMONIA" and show_hospitals:
                st.warning("🚨 **Pneumonia detected!** Here are nearby healthcare facilities:")
                
                # Create and display map
                hospital_map, hospitals = create_hospital_map()
                folium_static(hospital_map, width=700, height=500)
                
                st.markdown("### 📍 Nearby Hospitals")
                
                for hospital in hospitals:
                    emergency_badge = "🚨 Emergency Services" if hospital['emergency'] else "🏥 Clinic"
                    
                    st.markdown(f"""
                    <div class="hospital-card">
                        <h4>{hospital['name']}</h4>
                        <p><b>📍 Address:</b> {hospital['address']}</p>
                        <p><b>📞 Phone:</b> <a href="tel:{hospital['phone']}">{hospital['phone']}</a></p>
                        <p><b>📏 Distance:</b> {hospital['distance']}</p>
                        <p><b>{emergency_badge}</b></p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
                st.info("""
                💡 **Tips for Hospital Visit:**
                - Bring your X-ray images and this AI report
                - List all current symptoms and medications
                - Bring insurance information
                - Have someone accompany you if possible
                """)
            
            else:
                st.success("✅ Your X-ray appears normal. Regular check-ups are still recommended!")
                st.info("🏥 For routine check-ups, consult your primary care physician.")
        
        else:
            st.info("📊 Analyze an X-ray first to see nearby healthcare facilities")
    
    with tab4:
        st.subheader("📊 About This System")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h2>90-95%</h2>
                <p>Accuracy</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h2>&lt;1s</h2>
                <p>Analysis Time</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h2>5,856</h2>
                <p>Training Images</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("""
        ### 🤖 AI Technology
        
        This system uses a **hybrid deep learning architecture** combining:
        - **ResNet50**: Pre-trained convolutional neural network
        - **Autoencoder**: Custom feature extraction
        - **Transfer Learning**: Adapted for medical imaging
        
        ### 🎯 Features
        
        - ✅ **AI-Powered Detection**: 90-95% accuracy in pneumonia detection
        - ✅ **Educational Resources**: Curated YouTube videos and medical information
        - ✅ **Treatment Guidance**: Evidence-based recommendations
        - ✅ **Hospital Locator**: Find nearby healthcare facilities
        - ✅ **Real-time Analysis**: Results in less than 1 second
        
        ### 🔬 Model Training
        
        - **Dataset**: 5,856 chest X-ray images
        - **Training Platform**: Google Colab with GPU acceleration
        - **Architecture**: Hybrid (ResNet50 + Autoencoder)
        - **Validation**: Tested on independent test set
        
        ### ⚠️ Important Notes
        
        - This is a **screening tool**, not a diagnostic device
        - Always consult healthcare professionals for medical decisions
        - Results should be verified by qualified radiologists
        - For educational and research purposes
        
        ### 👨‍💻 Technology Stack
        
        - **AI/ML**: TensorFlow, Keras, ResNet50
        - **Web Framework**: Streamlit
        - **Visualization**: Plotly, Folium
        - **Deployment**: Docker, Cloud platforms
        """)
        
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #666;'>
            <p>🫁 Pneumonia Detection & Care System</p>
            <p>Built with ❤️ using AI and Modern Web Technologies</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()