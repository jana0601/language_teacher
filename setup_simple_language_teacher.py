#!/usr/bin/env python3
"""
Language Teacher Setup Script - Windows Compatible Version
Handles Ollama model download, service startup, and verification
"""

import subprocess
import time
import requests
import sys
import os
import json
from pathlib import Path

class LanguageTeacherSetup:
    def __init__(self):
        self.ollama_url = "http://localhost:11434"
        self.model_name = "llama3.2"
        self.setup_log = []
        
    def log(self, message, level="INFO"):
        """Log messages with timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        print(log_entry)
        self.setup_log.append(log_entry)
        
    def check_ollama_installed(self):
        """Check if Ollama is installed and accessible"""
        self.log("Checking if Ollama is installed...")
        
        try:
            result = subprocess.run(["ollama", "--version"], 
                                 capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                version = result.stdout.strip()
                self.log(f"SUCCESS: Ollama is installed: {version}")
                return True
            else:
                self.log(f"ERROR: Ollama command failed: {result.stderr}", "ERROR")
                return False
        except FileNotFoundError:
            self.log("ERROR: Ollama is not installed or not in PATH", "ERROR")
            return False
        except subprocess.TimeoutExpired:
            self.log("ERROR: Ollama command timed out", "ERROR")
            return False
        except Exception as e:
            self.log(f"ERROR: Error checking Ollama: {e}", "ERROR")
            return False
    
    def start_ollama_service(self):
        """Start Ollama service"""
        self.log("Starting Ollama service...")
        
        try:
            # Check if service is already running
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                self.log("SUCCESS: Ollama service is already running")
                return True
        except:
            pass
        
        try:
            # Start Ollama service in background
            process = subprocess.Popen(["ollama", "serve"], 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE)
            
            # Wait a moment for service to start
            time.sleep(3)
            
            # Check if service is now running
            for attempt in range(10):
                try:
                    response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
                    if response.status_code == 200:
                        self.log("SUCCESS: Ollama service started successfully")
                        return True
                except:
                    time.sleep(2)
                    
            self.log("ERROR: Failed to start Ollama service", "ERROR")
            return False
            
        except Exception as e:
            self.log(f"ERROR: Error starting Ollama service: {e}", "ERROR")
            return False
    
    def check_model_installed(self):
        """Check if the required model is installed"""
        self.log(f"Checking if {self.model_name} model is installed...")
        
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=10)
            if response.status_code == 200:
                models = response.json().get("models", [])
                for model in models:
                    if self.model_name in model.get("name", ""):
                        self.log(f"SUCCESS: Model {self.model_name} is already installed")
                        return True
                
                self.log(f"ERROR: Model {self.model_name} is not installed")
                return False
            else:
                self.log(f"ERROR: Failed to check models: HTTP {response.status_code}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"ERROR: Error checking models: {e}", "ERROR")
            return False
    
    def download_model(self):
        """Download the required model"""
        self.log(f"Downloading {self.model_name} model (this may take several minutes)...")
        
        try:
            # Start the download process
            process = subprocess.Popen(["ollama", "pull", self.model_name],
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT,
                                     text=True,
                                     universal_newlines=True)
            
            # Monitor download progress
            download_log = []
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    output = output.strip()
                    download_log.append(output)
                    if "pulling" in output.lower() or "downloading" in output.lower():
                        self.log(f"DOWNLOAD: {output}")
                    elif "success" in output.lower() or "pulled" in output.lower():
                        self.log(f"SUCCESS: {output}")
            
            # Check if download was successful
            if process.returncode == 0:
                self.log(f"SUCCESS: Model {self.model_name} downloaded successfully")
                return True
            else:
                self.log(f"ERROR: Model download failed with return code {process.returncode}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"ERROR: Error downloading model: {e}", "ERROR")
            return False
    
    def test_model(self):
        """Test the model with a simple query"""
        self.log("Testing model with a simple query...")
        
        try:
            test_payload = {
                "model": self.model_name,
                "prompt": "Hello, how are you?",
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "max_tokens": 50
                }
            }
            
            response = requests.post(f"{self.ollama_url}/api/generate",
                                   json=test_payload,
                                   timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if "response" in result:
                    self.log("SUCCESS: Model test successful")
                    self.log(f"Test response: {result['response'][:50]}...")
                    return True
            
            self.log(f"ERROR: Model test failed: HTTP {response.status_code}", "ERROR")
            return False
            
        except Exception as e:
            self.log(f"ERROR: Error testing model: {e}", "ERROR")
            return False
    
    def install_python_dependencies(self):
        """Install required Python packages"""
        self.log("Installing Python dependencies...")
        
        try:
            requirements_file = Path(__file__).parent / "backend" / "requirements.txt"
            if requirements_file.exists():
                result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
                                     capture_output=True, text=True, timeout=300)
                if result.returncode == 0:
                    self.log("SUCCESS: Python dependencies installed successfully")
                    return True
                else:
                    self.log(f"ERROR: Failed to install dependencies: {result.stderr}", "ERROR")
                    return False
            else:
                self.log("ERROR: Requirements file not found", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"ERROR: Error installing dependencies: {e}", "ERROR")
            return False
    
    def create_startup_script(self):
        """Create a startup script for easy launching"""
        self.log("Creating startup script...")
        
        startup_script = f"""@echo off
REM Language Teacher Startup Script
echo Starting Language Teacher...

REM Start Ollama service
echo Starting Ollama service...
start /b ollama serve

REM Wait for service to start
timeout /t 5 /nobreak >nul

REM Start the GUI
echo Starting Language Teacher GUI...
python gui_app.py

pause
"""
        
        try:
            script_path = Path(__file__).parent / "start_language_teacher.bat"
            with open(script_path, 'w') as f:
                f.write(startup_script)
            self.log(f"SUCCESS: Startup script created: {script_path}")
            return True
        except Exception as e:
            self.log(f"ERROR: Error creating startup script: {e}", "ERROR")
            return False
    
    def run_setup(self):
        """Run the complete setup process"""
        self.log("Starting Language Teacher Setup")
        self.log("=" * 50)
        
        # Step 1: Check Ollama installation
        if not self.check_ollama_installed():
            self.log("ERROR: Setup failed: Ollama is not installed", "ERROR")
            self.log("Please install Ollama from: https://ollama.ai", "ERROR")
            return False
        
        # Step 2: Start Ollama service
        if not self.start_ollama_service():
            self.log("ERROR: Setup failed: Cannot start Ollama service", "ERROR")
            return False
        
        # Step 3: Check if model is installed
        if not self.check_model_installed():
            # Step 4: Download model
            if not self.download_model():
                self.log("ERROR: Setup failed: Cannot download model", "ERROR")
                return False
        
        # Step 5: Test model
        if not self.test_model():
            self.log("ERROR: Setup failed: Model test failed", "ERROR")
            return False
        
        # Step 6: Install Python dependencies
        if not self.install_python_dependencies():
            self.log("ERROR: Setup failed: Cannot install Python dependencies", "ERROR")
            return False
        
        # Step 7: Create startup script
        self.create_startup_script()
        
        # Success!
        self.log("SUCCESS: Setup completed successfully!")
        self.log("=" * 50)
        self.log("Next steps:")
        self.log("1. Run: python gui_app.py")
        self.log("2. Or double-click: start_language_teacher.bat")
        self.log("3. Select a language and start chatting!")
        
        return True
    
    def save_log(self):
        """Save setup log to file"""
        try:
            log_file = Path(__file__).parent / "setup_log.txt"
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write("\n".join(self.setup_log))
            self.log(f"Setup log saved to: {log_file}")
        except Exception as e:
            self.log(f"Error saving log: {e}", "ERROR")

def main():
    """Main setup function"""
    setup = LanguageTeacherSetup()
    
    try:
        success = setup.run_setup()
        setup.save_log()
        
        if success:
            print("\nSUCCESS: Setup completed successfully!")
            print("You can now run the Language Teacher GUI!")
            print("\nTo start:")
            print("  python gui_app.py")
            print("  or double-click start_language_teacher.bat")
        else:
            print("\nERROR: Setup failed. Check the log above for details.")
            print("Setup log saved to setup_log.txt")
            
    except KeyboardInterrupt:
        print("\n\nWARNING: Setup interrupted by user")
        setup.save_log()
    except Exception as e:
        print(f"\nERROR: Unexpected error: {e}")
        setup.save_log()

if __name__ == "__main__":
    main()
