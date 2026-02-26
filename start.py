import subprocess
import sys
import time
import os

def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def start_backend():
    """Start the FastAPI backend."""
    print("🚀 Starting FastAPI backend...")
    try:
        # Start backend in background
        subprocess.Popen([sys.executable, "backend.py"])
        print("✅ Backend started on http://localhost:8000")
        return True
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return False

def start_frontend():
    """Start the Streamlit frontend."""
    print("🎨 Starting Streamlit frontend...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "frontend.py"])
        return True
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return False

def main():
    """Main startup function."""
    print("🚢 Titanic Dataset Chat Agent - Startup Script")
    print("=" * 50)
    
    # Check if dependencies are installed
    if not install_dependencies():
        return
    
    # Start backend
    if not start_backend():
        return
    
    # Wait a moment for backend to start
    print("⏳ Waiting for backend to initialize...")
    time.sleep(3)
    
    # Start frontend
    if not start_frontend():
        return
    
    print("\n🎉 Application started successfully!")
    print("📱 Open your browser to: http://localhost:8501")
    print("🔧 Backend API is running on: http://localhost:8000")

if __name__ == "__main__":
    main()
