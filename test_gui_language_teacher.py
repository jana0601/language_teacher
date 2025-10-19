#!/usr/bin/env python3
"""
Test script to verify Language Teacher GUI dependencies
"""

import sys
import os

# Add backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_imports():
    """Test all required imports"""
    print("🧪 Testing Language Teacher GUI Dependencies")
    print("=" * 50)
    
    # Test tkinter
    try:
        import tkinter as tk
        print("✅ tkinter - GUI framework")
    except ImportError as e:
        print(f"❌ tkinter - {e}")
        return False
    
    # Test backend modules
    try:
        from chat_handler import ChatHandler
        print("✅ chat_handler - Chat conversation logic")
    except ImportError as e:
        print(f"❌ chat_handler - {e}")
        return False
    
    try:
        from evaluator import LanguageEvaluator
        print("✅ evaluator - Language evaluation engine")
    except ImportError as e:
        print(f"❌ evaluator - {e}")
        return False
    
    # Test other dependencies
    try:
        import requests
        print("✅ requests - HTTP client")
    except ImportError as e:
        print(f"❌ requests - {e}")
        return False
    
    try:
        import flask
        print("✅ flask - Web framework")
    except ImportError as e:
        print(f"❌ flask - {e}")
        return False
    
    print("\n🎉 All dependencies are available!")
    return True

def test_ollama_connection():
    """Test connection to Ollama"""
    print("\n🔗 Testing Ollama Connection")
    print("=" * 30)
    
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama is running and accessible")
            return True
        else:
            print(f"⚠️  Ollama responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama")
        print("   Make sure Ollama is running: ollama serve")
        return False
    except Exception as e:
        print(f"❌ Error connecting to Ollama: {e}")
        return False

def main():
    """Main test function"""
    success = test_imports()
    
    if success:
        ollama_ok = test_ollama_connection()
        
        print("\n📋 Summary:")
        print("=" * 20)
        print("✅ Python dependencies: OK")
        if ollama_ok:
            print("✅ Ollama connection: OK")
            print("\n🚀 Ready to launch GUI!")
            print("Run: python gui_app.py")
        else:
            print("⚠️  Ollama connection: Failed")
            print("\n⚠️  GUI will work but may show errors")
            print("Run: python gui_app.py")
    else:
        print("\n❌ Missing dependencies - please install them first")
        print("Run: pip install -r backend/requirements.txt")

if __name__ == "__main__":
    main()
