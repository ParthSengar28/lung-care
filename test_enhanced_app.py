"""
Quick test script to verify enhanced app dependencies
"""
import sys

def test_imports():
    """Test all required imports"""
    print("🧪 Testing Enhanced App Dependencies")
    print("="*50)
    
    required_packages = [
        ('streamlit', 'Streamlit'),
        ('plotly.graph_objects', 'Plotly'),
        ('folium', 'Folium'),
        ('streamlit_folium', 'Streamlit-Folium'),
        ('tensorflow', 'TensorFlow'),
        ('PIL', 'Pillow'),
        ('numpy', 'NumPy'),
        ('pandas', 'Pandas'),
        ('matplotlib.pyplot', 'Matplotlib'),
        ('seaborn', 'Seaborn')
    ]
    
    failed = []
    
    for package, name in required_packages:
        try:
            __import__(package)
            print(f"✅ {name:20} - OK")
        except ImportError as e:
            print(f"❌ {name:20} - MISSING")
            failed.append(name)
    
    print("="*50)
    
    if failed:
        print(f"\n❌ Missing packages: {', '.join(failed)}")
        print("\nTo install missing packages:")
        print("pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All dependencies installed successfully!")
        print("\n🚀 You can now run:")
        print("streamlit run enhanced_web_app.py")
        return True

def test_models():
    """Test if models are available"""
    import os
    
    print("\n🧠 Testing Model Files")
    print("="*50)
    
    models_dir = "models"
    required_models = [
        "hybrid_model_colab.h5",
        "resnet_classifier_colab.h5",
        "encoder_colab.h5",
        "autoencoder_colab.h5"
    ]
    
    missing = []
    
    for model in required_models:
        model_path = os.path.join(models_dir, model)
        if os.path.exists(model_path):
            size = os.path.getsize(model_path) / (1024 * 1024)  # MB
            print(f"✅ {model:30} - {size:.1f} MB")
        else:
            print(f"❌ {model:30} - MISSING")
            missing.append(model)
    
    print("="*50)
    
    if missing:
        print(f"\n⚠️ Missing models: {', '.join(missing)}")
        print("\nThe app will run but AI detection won't work.")
        print("To fix: Run setup_local_models.py")
        return False
    else:
        print("\n✅ All models found!")
        return True

def main():
    print("🫁 Enhanced Pneumonia Detection App - Dependency Check")
    print("="*50)
    print()
    
    # Test imports
    imports_ok = test_imports()
    
    # Test models
    models_ok = test_models()
    
    print("\n" + "="*50)
    print("📊 SUMMARY")
    print("="*50)
    
    if imports_ok and models_ok:
        print("✅ Everything is ready!")
        print("\n🚀 Start your app with:")
        print("   streamlit run enhanced_web_app.py")
        print("\n🌐 Access at: http://localhost:8501")
    elif imports_ok and not models_ok:
        print("⚠️ Dependencies OK, but models missing")
        print("\n🚀 You can still run the app (features will work except AI detection):")
        print("   streamlit run enhanced_web_app.py")
    else:
        print("❌ Please install missing dependencies first:")
        print("   pip install -r requirements.txt")

if __name__ == "__main__":
    main()