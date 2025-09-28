#!/usr/bin/env python3
"""
Setup script for the Job Search Agent
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✓ Python version: {sys.version}")

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)

def setup_environment():
    """Setup environment file"""
    env_file = Path(".env")
    env_example = Path("env_example.txt")
    
    if not env_file.exists() and env_example.exists():
        shutil.copy(env_example, env_file)
        print("✓ Created .env file from template")
        print("⚠️  Please edit .env file with your credentials")
    elif env_file.exists():
        print("✓ .env file already exists")
    else:
        print("⚠️  No environment template found")

def create_directories():
    """Create necessary directories"""
    directories = ["job_reports", "logs"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Created directory: {directory}")

def check_chrome():
    """Check if Chrome is installed"""
    chrome_paths = [
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium-browser",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            print("✓ Chrome browser found")
            return True
    
    print("⚠️  Chrome browser not found. Please install Chrome for web scraping")
    return False

def verify_setup():
    """Verify the setup is complete"""
    print("\n" + "="*50)
    print("SETUP VERIFICATION")
    print("="*50)
    
    # Check required files
    required_files = [
        "config.py",
        "linkedin_scraper.py",
        "glassdoor_scraper.py",
        "apollo_enricher.py",
        "data_processor.py",
        "report_generator.py",
        "job_search_agent.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✓ All required files present")
    
    # Check environment file
    if Path(".env").exists():
        print("✓ Environment file exists")
    else:
        print("❌ Environment file missing")
        return False
    
    # Check directories
    if Path("job_reports").exists():
        print("✓ Output directory exists")
    else:
        print("❌ Output directory missing")
        return False
    
    print("\n✓ Setup verification completed successfully!")
    return True

def main():
    """Main setup function"""
    print("Job Search Agent Setup")
    print("="*30)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Setup environment
    setup_environment()
    
    # Create directories
    create_directories()
    
    # Check Chrome
    check_chrome()
    
    # Verify setup
    if verify_setup():
        print("\n" + "="*50)
        print("SETUP COMPLETED SUCCESSFULLY!")
        print("="*50)
        print("\nNext steps:")
        print("1. Edit .env file with your credentials")
        print("2. Configure search parameters in config.py")
        print("3. Run: python job_search_agent.py once")
        print("4. Or run with scheduler: python job_search_agent.py")
        print("\nFor more information, see README.md")
    else:
        print("\n❌ Setup verification failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
