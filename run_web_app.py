#!/usr/bin/env python3
"""
CareerGuideAI Web Application Startup Script
Installs dependencies and launches the web application.
"""

import subprocess
import sys
import os
from pathlib import Path

def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import flask
        print("✅ Flask is installed")
        return True
    except ImportError:
        print("❌ Flask is not installed")
        return False

def create_directories():
    """Create necessary directories if they don't exist."""
    directories = ['templates', 'static', 'output']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("✅ Directories created/verified")

def main():
    """Main startup function."""
    print("🚀 CareerGuideAI Web Application Startup")
    print("=" * 50)
    
    # Create necessary directories
    create_directories()
    
    # Check if dependencies are installed
    if not check_dependencies():
        print("\n📦 Installing missing dependencies...")
        if not install_dependencies():
            print("❌ Failed to install dependencies. Please install manually:")
            print("   pip install -r requirements.txt")
            return
    
    print("\n🌐 Starting CareerGuideAI Web Application...")
    print("📱 The application will be available at: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Import and run the Flask app
        from app import app
        print("🚀 CareerGuideAI Web Application Starting...")
        print("📱 Available at: http://127.0.0.1:5000")
        print("🌐 Also try: http://localhost:5000")
        print("🌐 Network access: http://10.58.30.179:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("Please check if all files are in the correct location")

if __name__ == "__main__":
    main() 