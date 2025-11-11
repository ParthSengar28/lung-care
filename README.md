# Pneumonia Detection using ResNet50 with Autoencoding

An end-to-end deep learning project for detecting pneumonia in chest X-ray images using a hybrid approach combining ResNet50 and autoencoder features.

## Project Overview

This project implements three different approaches for pneumonia detection:

1. **Autoencoder**: For feature extraction and image denoising
2. **ResNet50 Classifier**: Pre-trained ResNet50 with custom classification head
3. **Hybrid Model**: Combines autoencoder features with ResNet50 for maximum accuracy

## Project Structure

```
pneumonia_detection/
├── config/
│   └── config.py              # Configuration settings
├── src/
│   ├── models/
│   │   ├── autoencoder.py     # Autoencoder model
│   │   ├── resnet_classifier.py # ResNet50 classifier
│   │   └── hybrid_model.py    # Hybrid model combining both
│   ├── data/
│   │   └── data_loader.py     # Data loading and preprocessing
│   ├── training/
│   │   ├── train_autoencoder.py # Autoencoder training
│   │   ├── train_classifier.py  # ResNet50 training
│   │   └── train_hybrid.py     # Hybrid model training
│   └── utils/
│       └── metrics.py         # Evaluation metrics and visualization
├── data/
│   └── chest_xray/           # Dataset directory
├── models/                   # Saved models directory
├── results/                  # Training results and plots
├── main.py                   # Main training pipeline
├── inference.py              # Inference script
└── requirements.txt          # Dependencies
```

## Installation

1. Clone the repository and navigate to the project directory
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Dataset

The project expects the chest X-ray dataset in the following structure:

```
data/chest_xray/
├── train/
│   ├── NORMAL/
│   └── PNEUMONIA/
├── val/
│   ├── NORMAL/
│   └── PNEUMONIA/
└── test/
    ├── NORMAL/
    └── PNEUMONIA/
```

## Usage

### Training

#### Train All Models (Recommended)

```bash
python main.py --mode all --fine_tune
```

#### Train Individual Models

```bash
# Train autoencoder only
python main.py --mode autoencoder

# Train ResNet50 classifier only
python main.py --mode classifier --fine_tune

# Train hybrid model only (requires pre-trained autoencoder)
python main.py --mode hybrid
```

### Inference

#### Single Image Prediction

```bash
python inference.py --image path/to/xray_image.jpg
```

#### Batch Prediction

```bash
python inference.py --batch path/to/images_directory/
```

#### Use Specific Model

```bash
python inference.py --image path/to/image.jpg --model models/hybrid_model.h5
```

## Model Architecture

### Autoencoder

- **Encoder**: 4 convolutional blocks with batch normalization and max pooling
- **Decoder**: 4 deconvolutional blocks with upsampling
- **Purpose**: Feature extraction and image denoising

### ResNet50 Classifier

- **Base**: Pre-trained ResNet50 (ImageNet weights)
- **Head**: Global average pooling + dense layers with dropout
- **Training**: Two-phase training (frozen → fine-tuned)

### Hybrid Model

- **Features**: Combines autoencoder and ResNet50 features
- **Architecture**: Concatenated features → dense classification head
- **Advantage**: Leverages both learned representations

## Configuration

Modify `config/config.py` to adjust:

- Image dimensions
- Batch size
- Learning rates
- Training epochs
- Model paths

## Results

Training results are saved in the `results/` directory:

- Training history plots
- Model evaluation metrics
- Confusion matrices
- ROC curves

## Key Features

- **Data Augmentation**: Rotation, shifting, flipping, zooming
- **Transfer Learning**: Pre-trained ResNet50 weights
- **Two-Phase Training**: Frozen → fine-tuned approach
- **Early Stopping**: Prevents overfitting
- **Model Checkpointing**: Saves best models automatically
- **Comprehensive Evaluation**: Multiple metrics and visualizations

## Performance Optimization

The hybrid approach typically achieves the highest accuracy by:

1. Using autoencoder features for noise reduction
2. Leveraging ResNet50's powerful feature extraction
3. Combining complementary representations
4. Fine-tuning for domain-specific features

## Requirements

- Python 3.7+
- TensorFlow 2.x
- GPU recommended for training

## License

This project is for educational and research purposes.
