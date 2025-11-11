"""
Laptop-friendly inference script
"""
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt
import argparse
import os
from config.ultra_light_config import UltraLightConfig

class LaptopPneumoniaDetector:
    def __init__(self):
        self.config = UltraLightConfig()
        
        if not os.path.exists(self.config.CLASSIFIER_PATH):
            raise FileNotFoundError(f"Model not found at {self.config.CLASSIFIER_PATH}. Please train the model first using laptop_train.py")
        
        print("Loading laptop-trained model...")
        self.model = load_model(self.config.CLASSIFIER_PATH)
        print("✅ Model loaded successfully!")
    
    def preprocess_image(self, img_path):
        """Preprocess image for laptop model"""
        img = image.load_img(img_path, target_size=(self.config.IMG_HEIGHT, self.config.IMG_WIDTH))
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
        
        class_name = self.config.CLASSES[predicted_class]
        
        if show_image:
            plt.figure(figsize=(6, 4))
            plt.imshow(original_img)
            plt.title(f'Laptop Prediction: {class_name}\nConfidence: {confidence:.2%}')
            plt.axis('off')
            plt.show()
        
        return {
            'class': class_name,
            'confidence': float(confidence),
            'probabilities': {
                self.config.CLASSES[i]: float(prediction[0][i]) 
                for i in range(len(self.config.CLASSES))
            }
        }

def main():
    parser = argparse.ArgumentParser(description='Laptop Pneumonia Detection')
    parser.add_argument('--image', type=str, required=True, help='Path to X-ray image')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.image):
        print(f"❌ Image not found: {args.image}")
        return
    
    try:
        detector = LaptopPneumoniaDetector()
        result = detector.predict(args.image)
        
        print(f"\n🔍 Prediction Results:")
        print(f"Class: {result['class']}")
        print(f"Confidence: {result['confidence']:.2%}")
        print(f"Probabilities: {result['probabilities']}")
        
    except Exception as e:
        print(f"❌ Prediction failed: {str(e)}")

if __name__ == "__main__":
    main()