"""
Deployment script for Pneumonia Detection System
Supports multiple deployment options
"""
import os
import subprocess
import sys
import argparse
import shutil
from pathlib import Path

class PneumoniaDetectionDeployer:
    def __init__(self):
        self.project_root = Path.cwd()
        self.models_dir = self.project_root / "models"
        
    def check_requirements(self):
        """Check if all requirements are met"""
        print("🔍 Checking deployment requirements...")
        
        # Check if models exist
        required_models = [
            "hybrid_model_colab.h5",
            "resnet_classifier_colab.h5",
            "encoder_colab.h5"
        ]
        
        missing_models = []
        for model in required_models:
            if not (self.models_dir / model).exists():
                missing_models.append(model)
        
        if missing_models:
            print(f"❌ Missing models: {', '.join(missing_models)}")
            print("Please ensure your trained models are in the 'models' directory")
            return False
        
        print("✅ All required models found")
        
        # Check Python version
        if sys.version_info < (3, 8):
            print("❌ Python 3.8+ required")
            return False
        
        print("✅ Python version compatible")
        return True
    
    def install_dependencies(self):
        """Install required dependencies"""
        print("📦 Installing dependencies...")
        
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", "requirements_web.txt"
            ], check=True)
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False
    
    def deploy_local(self, mode="web"):
        """Deploy locally"""
        print(f"🚀 Deploying locally in {mode} mode...")
        
        if mode == "web":
            print("Starting Streamlit web application...")
            print("🌐 Web app will be available at: http://localhost:8501")
            subprocess.run([
                sys.executable, "-m", "streamlit", "run", "web_app.py",
                "--server.port=8501",
                "--server.address=0.0.0.0"
            ])
        
        elif mode == "api":
            print("Starting FastAPI server...")
            print("🔗 API will be available at: http://localhost:8000")
            print("📚 API docs at: http://localhost:8000/docs")
            subprocess.run([
                sys.executable, "-m", "uvicorn", "api_server:app",
                "--host", "0.0.0.0",
                "--port", "8000",
                "--reload"
            ])
        
        elif mode == "both":
            print("Starting both web app and API...")
            print("🌐 Web app: http://localhost:8501")
            print("🔗 API: http://localhost:8000")
            
            # Start API in background
            api_process = subprocess.Popen([
                sys.executable, "-m", "uvicorn", "api_server:app",
                "--host", "0.0.0.0",
                "--port", "8000"
            ])
            
            # Start web app
            try:
                subprocess.run([
                    sys.executable, "-m", "streamlit", "run", "web_app.py",
                    "--server.port=8501",
                    "--server.address=0.0.0.0"
                ])
            finally:
                api_process.terminate()
    
    def deploy_docker(self):
        """Deploy using Docker"""
        print("🐳 Deploying with Docker...")
        
        # Check if Docker is available
        try:
            subprocess.run(["docker", "--version"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Docker not found. Please install Docker first.")
            return False
        
        # Build and run with docker-compose
        try:
            print("Building Docker images...")
            subprocess.run(["docker-compose", "build"], check=True)
            
            print("Starting services...")
            subprocess.run(["docker-compose", "up", "-d"], check=True)
            
            print("✅ Docker deployment successful!")
            print("🌐 Web app: http://localhost:8501")
            print("🔗 API: http://localhost:8000")
            print("📚 API docs: http://localhost:8000/docs")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Docker deployment failed: {e}")
            return False
    
    def deploy_heroku(self):
        """Deploy to Heroku"""
        print("☁️ Preparing Heroku deployment...")
        
        # Create Procfile
        procfile_content = """web: streamlit run web_app.py --server.port=$PORT --server.address=0.0.0.0
api: uvicorn api_server:app --host=0.0.0.0 --port=$PORT"""
        
        with open("Procfile", "w") as f:
            f.write(procfile_content)
        
        # Create runtime.txt
        with open("runtime.txt", "w") as f:
            f.write("python-3.9.18")
        
        print("✅ Heroku files created")
        print("📋 Next steps for Heroku deployment:")
        print("1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli")
        print("2. Login: heroku login")
        print("3. Create app: heroku create your-app-name")
        print("4. Deploy: git push heroku main")
        print("5. Scale: heroku ps:scale web=1")
    
    def create_deployment_package(self):
        """Create a deployment package"""
        print("📦 Creating deployment package...")
        
        package_dir = Path("pneumonia_detection_package")
        if package_dir.exists():
            shutil.rmtree(package_dir)
        
        package_dir.mkdir()
        
        # Copy essential files
        essential_files = [
            "web_app.py",
            "api_server.py",
            "colab_local_inference.py",
            "requirements_web.txt",
            "Dockerfile",
            "docker-compose.yml",
            "README.md"
        ]
        
        for file in essential_files:
            if Path(file).exists():
                shutil.copy2(file, package_dir)
        
        # Copy models directory
        if self.models_dir.exists():
            shutil.copytree(self.models_dir, package_dir / "models")
        
        # Create deployment instructions
        instructions = """
# Pneumonia Detection Deployment Package

## Quick Start

### Option 1: Web Application
```bash
pip install -r requirements_web.txt
streamlit run web_app.py
```
Access at: http://localhost:8501

### Option 2: API Server
```bash
pip install -r requirements_web.txt
python api_server.py
```
Access at: http://localhost:8000

### Option 3: Docker
```bash
docker-compose up
```
Web: http://localhost:8501
API: http://localhost:8000

## Files Included
- web_app.py: Streamlit web interface
- api_server.py: FastAPI backend
- models/: Trained AI models
- requirements_web.txt: Dependencies
- Dockerfile & docker-compose.yml: Container deployment

## Support
For issues, check the main project documentation.
"""
        
        with open(package_dir / "DEPLOYMENT.md", "w") as f:
            f.write(instructions)
        
        print(f"✅ Deployment package created: {package_dir}")
        return package_dir

def main():
    parser = argparse.ArgumentParser(description="Deploy Pneumonia Detection System")
    parser.add_argument("--mode", choices=["web", "api", "both", "docker", "heroku", "package"], 
                       default="web", help="Deployment mode")
    parser.add_argument("--skip-deps", action="store_true", help="Skip dependency installation")
    
    args = parser.parse_args()
    
    deployer = PneumoniaDetectionDeployer()
    
    print("🫁 Pneumonia Detection System Deployment")
    print("="*50)
    
    # Check requirements
    if not deployer.check_requirements():
        print("❌ Requirements check failed")
        return
    
    # Install dependencies
    if not args.skip_deps:
        if not deployer.install_dependencies():
            print("❌ Dependency installation failed")
            return
    
    # Deploy based on mode
    if args.mode == "docker":
        deployer.deploy_docker()
    elif args.mode == "heroku":
        deployer.deploy_heroku()
    elif args.mode == "package":
        deployer.create_deployment_package()
    else:
        deployer.deploy_local(args.mode)

if __name__ == "__main__":
    main()