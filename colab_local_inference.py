"""
Local inference script for Colab-trained models
Use this script on your laptop with models trained on Google Colab
"""
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt
import argparse
import os

class ColabTrainedDetector:
    def __init__(self, models_dir="models"):
        self.models_dir = models_dir
        self.img_height = 224
        self.img_width = 224
        self.classes = ['NORMAL', 'PNEUMONIA']
        
        # Try to load the best available model
        self.model = self.load_best_model()
    
    def load_best_model(self):
        """Load the best available Colab-trained model"""
        
        model_files = [
            ("Hybrid Model", os.path.join(self.models_dir, "hybrid_model_colab.h5")),
            ("ResNet50 Classifier", os.path.join(self.models_dir, "resnet_classifier_colab.h5")),
            ("Autoencoder", os.path.join(self.models_dir, "autoencoder_colab.h5"))
        ]
        
        for model_name, model_path in model_files:
            if os.path.exists(model_path):
                print(f"Loading {model_name} from {model_path}")
                try:
                    model = load_model(model_path)
                    print(f"✅ {model_name} loaded successfully!")
                    return model
                except Exception as e:
                    print(f"❌ Failed to load {model_name}: {str(e)}")
                    continue
        
        raise FileNotFoundError(
            "No Colab-trained models found. Please ensure you have:\n"
            "1. Trained models on Google Colab\n"
            "2. Downloaded the models ZIP file\n"
            "3. Extracted the models to the 'models' directory"
        )
    
    def preprocess_image(self, img_path):
        """Preprocess image for Colab-trained model"""
        
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"Image not found: {img_path}")
        
        img = image.load_img(img_path, target_size=(self.img_height, self.img_width))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0
        
        return img_array, img
    
    def predict(self, img_path, show_image=True):
        """Make prediction on a single image"""
        
        img_array, original_img = self.preprocess_image(img_path)
        
        # Make prediction
        prediction = self.model.predict(img_array, verbose=0)
        predicted_class = np.argmax(prediction[0])
        confidence = prediction[0][predicted_class]
        
        class_name = self.classes[predicted_class]
        
        if show_image:
            plt.figure(figsize=(10, 6))
            plt.imshow(original_img)
            plt.title(f'Colab-Trained Model Prediction\n{class_name}\nConfidence: {confidence:.2%}', 
                     fontsize=16, fontweight='bold')
            plt.axis('off')
            plt.tight_layout()
            plt.show()
        
        return {
            'class': class_name,
            'confidence': float(confidence),
            'probabilities': {
                self.classes[i]: float(prediction[0][i]) 
                for i in range(len(self.classes))
            }
        }
    
    def predict_batch(self, img_paths):
        """Make predictions on multiple images"""
        
        results = []
        print(f"Processing {len(img_paths)} images...")
        
        for i, img_path in enumerate(img_paths, 1):
            try:
                result = self.predict(img_path, show_image=False)
                result['image_path'] = img_path
                results.append(result)
                
                print(f"[{i}/{len(img_paths)}] {os.path.basename(img_path)}: "
                      f"{result['class']} ({result['confidence']:.2%})")
                
            except Exception as e:
                print(f"❌ Error processing {img_path}: {str(e)}")
        
        return results
    
    def batch_analysis(self, results):
        """Analyze batch prediction results"""
        
        if not results:
            print("No results to analyze")
            return
        
        # Count predictions
        normal_count = sum(1 for r in results if r['class'] == 'NORMAL')
        pneumonia_count = len(results) - normal_count
        
        # Calculate average confidence
        avg_confidence = np.mean([r['confidence'] for r in results])
        
        # Find high and low confidence predictions
        high_conf = [r for r in results if r['confidence'] > 0.9]
        low_conf = [r for r in results if r['confidence'] < 0.7]
        
        print(f"\n📊 BATCH ANALYSIS RESULTS")
        print("="*50)
        print(f"Total images processed: {len(results)}")
        print(f"Normal predictions: {normal_count} ({normal_count/len(results)*100:.1f}%)")
        print(f"Pneumonia predictions: {pneumonia_count} ({pneumonia_count/len(results)*100:.1f}%)")
        print(f"Average confidence: {avg_confidence:.2%}")
        print(f"High confidence (>90%): {len(high_conf)} images")
        print(f"Low confidence (<70%): {len(low_conf)} images")
        
        if low_conf:
            print(f"\n⚠️ Low confidence predictions:")
            for r in low_conf[:5]:  # Show first 5
                print(f"  {os.path.basename(r['image_path'])}: {r['class']} ({r['confidence']:.2%})")

def setup_models_directory():
    """Help user set up models directory"""
    
    models_dir = "models"
    
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
        print(f"✅ Created {models_dir} directory")
    
    # Check for model files
    expected_models = [
        "hybrid_model_colab.h5",
        "resnet_classifier_colab.h5", 
        "autoencoder_colab.h5",
        "encoder_colab.h5"
    ]
    
    found_models = []
    for model_file in expected_models:
        model_path = os.path.join(models_dir, model_file)
        if os.path.exists(model_path):
            found_models.append(model_file)
    
    if found_models:
        print(f"✅ Found {len(found_models)} model files:")
        for model in found_models:
            print(f"  - {model}")
    else:
        print(f"❌ No model files found in {models_dir}/")
        print("\n📋 To use this script:")
        print("1. Train your models on Google Colab using colab_train.ipynb")
        print("2. Download the trained_pneumonia_models.zip file")
        print("3. Extract the ZIP file contents to the 'models' directory")
        print("4. Run this script again")
        
        return False
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Colab-Trained Pneumonia Detection')
    parser.add_argument('--image', type=str, help='Path to single image')
    parser.add_argument('--batch', type=str, help='Path to directory containing images')
    parser.add_argument('--models_dir', type=str, default='models', help='Directory containing trained models')
    
    args = parser.parse_args()
    
    print("🌐 Colab-Trained Pneumonia Detection")
    print("="*50)
    
    # Setup models directory
    if not setup_models_directory():
        return
    
    try:
        # Initialize detector
        detector = ColabTrainedDetector(args.models_dir)
        
        if args.image:
            # Single image prediction
            print(f"\n🔍 Analyzing: {args.image}")
            result = detector.predict(args.image)
            
            print(f"\n📋 Prediction Results:")
            print(f"Class: {result['class']}")
            print(f"Confidence: {result['confidence']:.2%}")
            print(f"\n📊 Detailed Probabilities:")
            for class_name, prob in result['probabilities'].items():
                print(f"  {class_name}: {prob:.2%}")
        
        elif args.batch:
            # Batch prediction
            if not os.path.exists(args.batch):
                print(f"❌ Directory not found: {args.batch}")
                return
            
            # Get all image files
            img_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
            img_paths = []
            
            for file in os.listdir(args.batch):
                if any(file.lower().endswith(ext) for ext in img_extensions):
                    img_paths.append(os.path.join(args.batch, file))
            
            if not img_paths:
                print(f"❌ No image files found in {args.batch}")
                return
            
            # Process batch
            results = detector.predict_batch(img_paths)
            detector.batch_analysis(results)
        
        else:
            print("Please provide either --image or --batch argument")
            print("\nExamples:")
            print("  python colab_local_inference.py --image data/test/NORMAL/IM-0001-0001.jpeg")
            print("  python colab_local_inference.py --batch data/test/NORMAL/")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Ensure you have trained models from Google Colab")
        print("2. Check that model files are in the correct directory")
        print("3. Verify image paths are correct")

if __name__ == "__main__":
    main()