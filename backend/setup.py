#!/usr/bin/env python3
"""
Setup script for AI Quarterly Reports application
Creates sample data and initializes the environment
"""

import os
import sys
import shutil
from pathlib import Path

def create_env_file():
    """Create .env file from template"""
    env_template = Path(".env.example")
    env_file = Path(".env")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return
    
    if not env_template.exists():
        print("❌ .env.example not found")
        return
    
    # Copy template to .env
    shutil.copy(env_template, env_file)
    print("✅ Created .env file from template")
    print("🔧 Please edit .env and add your GEMINI_API_KEY")

def create_sample_data():
    """Create sample market data"""
    try:
        # Import and run the sample data creation
        from create_sample_data import create_sample_data
        result = create_sample_data()
        print("✅ Sample market data created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create sample data: {e}")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'pandas', 
        'numpy',
        'google-generativeai',
        'chromadb',
        'python-dotenv',
        'pydantic',
        'sentence-transformers'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("✅ All required packages are installed")
        return True

def main():
    """Main setup function"""
    print("🚀 Setting up AI Quarterly Reports application...")
    print("=" * 50)
    
    # Change to backend directory
    os.chdir(Path(__file__).parent)
    
    # Check dependencies
    if not check_dependencies():
        print("\n💡 Install dependencies first:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    # Create sample data
    create_sample_data()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file and add your GEMINI_API_KEY")
    print("2. Start the backend: uvicorn main:app --reload")
    print("3. Start the frontend: cd ../frontend && npm install && npm run dev")
    print("\n🌐 Frontend: http://localhost:3000")
    print("🔗 Backend: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")

if __name__ == "__main__":
    main()