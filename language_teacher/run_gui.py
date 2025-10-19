#!/usr/bin/env python3
"""
Language Teacher GUI Launcher
Simple script to launch the Language Teacher GUI application
"""

import sys
import os
import subprocess
import tkinter as tk
from tkinter import messagebox

def check_ollama():
    """Check if Ollama is running"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def check_dependencies():
    """Check if required Python packages are installed"""
    required_packages = ['flask', 'requests', 'tkinter']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'tkinter':
                import tkinter
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def show_ollama_warning():
    """Show warning about Ollama not running"""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    message = """Ollama is not running!

To use the Language Teacher GUI, you need to:

1. Install Ollama from: https://ollama.ai
2. Pull the model: ollama pull llama3.2
3. Start Ollama: ollama serve

Would you like to continue anyway? (The app will show errors if Ollama is not running)"""
    
    result = messagebox.askyesno("Ollama Not Running", message)
    root.destroy()
    return result

def main():
    """Main launcher function"""
    print("🌍 Language Teacher GUI Launcher")
    print("=" * 40)
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("Installing missing packages...")
        
        for package in missing:
            if package != 'tkinter':  # tkinter comes with Python
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                    print(f"✅ Installed {package}")
                except subprocess.CalledProcessError:
                    print(f"❌ Failed to install {package}")
                    return
    
    # Check Ollama
    if not check_ollama():
        print("⚠️  Ollama is not running!")
        if not show_ollama_warning():
            print("Exiting...")
            return
    
    # Launch the GUI
    print("🚀 Launching Language Teacher GUI...")
    try:
        # Change to the correct directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # Import and run the GUI
        import gui_app
        gui_app.main()
        
    except Exception as e:
        print(f"❌ Error launching GUI: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
