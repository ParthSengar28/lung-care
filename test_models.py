"""
Test script to verify your Colab-trained models work locally
"""
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt

def test_model_loading():
    """Test if all models can be loaded successfully"""
    
    print("🧪 Testing Colab-trained models locally")
    print("="*50)
    
    models_dir = "models"
    model_files = {
        "Autoencoder": "autoencoder_colab.h5",
        "Encoder": "encoder_colab.h5",
        "ResNet50 Classifier": "resnet_classifier_colab.h5", 
        "Hybrid Model": "hybrid_model_colab.h5"
    }
    
    loaded_models = {}
    
    for model_name, model_file in model_files.items():
        model_path = os.path.join(models_dir, model_file)
        
        if os.path.exists(model_path):
            try:
                print(f"Loading {model_name}...")
                model = load_model(model_path)
                loaded_models[model_name] = model
                print(f"✅ {model_name} loaded successfully!")
                
                # Show model info
                total_params = model.count_params()
                print(f"   Parameters: {total_params:,}")
                print(f"   Input shape: {model.input_shape}")
                print(f"   Output shape: {model.output_shape}")
                
            except Exception as e:
                print(f"❌ Failed to load {model_name}: {str(e)}")
        else:
            print(f"❌ {model_name} file not found: {model_path}")
        
        print()
    
    return loaded_models

def test_prediction_on_sample():
    """Test prediction on a sample image from your dataset"""
    
    print("🔍 Testing prediction on sample image")
    print("="*50)
    
    # Try to load the best model (hybrid)
    models_dir = "models"
    hybrid_path = os.path.join(models_dir, "hybrid_model_colab.h5")
    classifier_path = os.path.join(models_dir, "resnet_classifier_colab.h5")
    
    model = None
    model_name = ""
    
    if os.path.exists(hybrid_path):
        model = load_model(hybrid_path)
        model_name = "Hybrid Model"
    elif os.path.exists(classifier_path):
        model = load_model(classifier_path)
        model_name = "ResNet50 Classifier"
    else:
        print("❌ No classifier models found")
        return
    
    print(f"Using {model_name} for prediction test")
    
    # Look for a sample image in your dataset
    sample_paths = [
        "data/chest_xray/test/NORMAL",
        "data/chest_xray/test/PNEUMONIA",
        "data/test/NORMAL",
        "data/test/PNEUMONIA"
    ]
    
    sample_image = None
    true_label = ""
    
    for path in sample_paths:
        if os.path.exists(path):
            image_files = [f for f in os.listdir(path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            if image_files:
                sample_image = os.path.join(path, image_files[0])
                true_label = "NORMAL" if "NORMAL" in path else "PNEUMONIA"
                break
    
    if not sample_image:
        print("❌ No sample images found in dataset")
        print("Please ensure your dataset is in data/chest_xray/ or data/")
        return
    
    print(f"Testing with: {sample_image}")
    print(f"True label: {true_label}")
    
    # Preprocess image
    img = image.load_img(sample_image, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    
    # Make prediction
    prediction = model.predict(img_array, verbose=0)
    predicted_class = np.argmax(prediction[0])
    confidence = prediction[0][predicted_class]
    
    classes = ['NORMAL', 'PNEUMONIA']
    predicted_label = classes[predicted_class]
    
    print(f"\\n📊 Prediction Results:")
    print(f"Predicted: {predicted_label}")
    print(f"Confidence: {confidence:.2%}")
    print(f"Correct: {'✅' if predicted_label == true_label else '❌'}")
    
    # Show detailed probabilities
    print(f"\\nDetailed probabilities:")
    for i, class_name in enumerate(classes):
        prob = prediction[0][i]
        print(f"  {class_name}: {prob:.2%}")
    
    # Display image
    plt.figure(figsize=(8, 6))
    plt.imshow(img)
    plt.title(f'Test Prediction\\nTrue: {true_label} | Predicted: {predicted_label}\\nConfidence: {confidence:.2%}')
    plt.axis('off')
    plt.show()
    
    print("✅ Prediction test completed!")

def main():
    print("🚀 Colab-Trained Model Testing Suite")
    print("="*60)
    
    # Test 1: Model loading
    loaded_models = test_model_loading()
    
    if not loaded_models:
        print("❌ No models could be loaded. Please check your setup.")
        return
    
    print("\\n" + "="*60)
    
    # Test 2: Sample prediction
    test_prediction_on_sample()
    
    print("\\n" + "="*60)
    print("🎉 All tests completed!")
    print("\\n📋 Next steps:")
    print("1. Use colab_local_inference.py for single image predictions")
    print("2. Use colab_local_inference.py --batch for multiple images")
    print("3. Integrate models into your own applications")

if __name__ == "__main__":
    main()