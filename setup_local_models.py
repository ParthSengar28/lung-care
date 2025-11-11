"""
Setup script to prepare your local environment for using Colab-trained models
"""
import os
import zipfile
import shutil

def setup_local_models():
    """Set up local environment for Colab-trained models"""
    
    print("🔧 Setting up local environment for Colab-trained models")
    print("="*60)
    
    # Create models directory
    models_dir = "models"
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
        print(f"✅ Created {models_dir} directory")
    else:
        print(f"✅ {models_dir} directory already exists")
    
    # Look for downloaded ZIP file
    zip_files = [f for f in os.listdir('.') if f.endswith('.zip') and 'pneumonia' in f.lower()]
    
    if zip_files:
        zip_file = zip_files[0]  # Use the first matching ZIP file
        print(f"📦 Found model ZIP file: {zip_file}")
        
        # Extract models
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(models_dir)
        
        print(f"✅ Models extracted to {models_dir}/")
        
        # List extracted files
        print("📁 Extracted model files:")
        for file in os.listdir(models_dir):
            if file.endswith('.h5'):
                file_path = os.path.join(models_dir, file)
                file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
                print(f"  - {file} ({file_size:.1f} MB)")
        
        # Clean up ZIP file
        os.remove(zip_file)
        print(f"🗑️ Removed {zip_file}")
        
    else:
        print("❌ No model ZIP file found in current directory")
        print("Please download the trained_pneumonia_models_gdrive.zip from Colab")
        return False
    
    # Verify model files
    expected_models = [
        "autoencoder_colab.h5",
        "encoder_colab.h5", 
        "resnet_classifier_colab.h5",
        "hybrid_model_colab.h5"
    ]
    
    missing_models = []
    for model in expected_models:
        model_path = os.path.join(models_dir, model)
        if not os.path.exists(model_path):
            missing_models.append(model)
    
    if missing_models:
        print(f"⚠️ Missing models: {', '.join(missing_models)}")
    else:
        print("✅ All expected models found!")
    
    print("\n🎯 Setup complete! You can now use your trained models locally.")
    return True

if __name__ == "__main__":
    setup_local_models()