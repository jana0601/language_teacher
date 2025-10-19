#!/usr/bin/env python3
"""
Language Teacher Verification Script
Tests all components after setup
"""

import requests
import subprocess
import sys
import os
import json

def test_ollama_service():
    """Test if Ollama service is running"""
    print("🔗 Testing Ollama service...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama service is running")
            return True
        else:
            print(f"❌ Ollama service error: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to Ollama: {e}")
        return False

def test_model():
    """Test if llama3.2 model is available"""
    print("🤖 Testing llama3.2 model...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            for model in models:
                if "llama3.2" in model.get("name", ""):
                    print("✅ llama3.2 model is available")
                    return True
            
            print("❌ llama3.2 model not found")
            print("Available models:")
            for model in models:
                print(f"  - {model.get('name', 'Unknown')}")
            return False
        else:
            print(f"❌ Cannot get model list: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing model: {e}")
        return False

def test_model_response():
    """Test if model can generate responses"""
    print("💬 Testing model response...")
    try:
        payload = {
            "model": "llama3.2",
            "prompt": "Hello, how are you?",
            "stream": False,
            "options": {
                "temperature": 0.7,
                "max_tokens": 50
            }
        }
        
        response = requests.post("http://localhost:11434/api/generate",
                               json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if "response" in result:
                print("✅ Model can generate responses")
                print(f"Test response: {result['response'][:100]}...")
                return True
            else:
                print("❌ No response in model output")
                return False
        else:
            print(f"❌ Model response error: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing model response: {e}")
        return False

def test_python_dependencies():
    """Test if Python dependencies are installed"""
    print("🐍 Testing Python dependencies...")
    
    dependencies = [
        ("flask", "Flask"),
        ("requests", "requests"),
        ("tkinter", "tkinter")
    ]
    
    all_ok = True
    for module, name in dependencies:
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} - not installed")
            all_ok = False
    
    return all_ok

def test_gui_imports():
    """Test if GUI can import all modules"""
    print("🖥️ Testing GUI imports...")
    
    try:
        # Add backend to path
        sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
        
        from chat_handler import ChatHandler
        print("✅ chat_handler")
        
        from evaluator import LanguageEvaluator
        print("✅ evaluator")
        
        import gui_app
        print("✅ gui_app")
        
        return True
    except Exception as e:
        print(f"❌ GUI import error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Language Teacher Verification")
    print("=" * 40)
    print()
    
    tests = [
        ("Ollama Service", test_ollama_service),
        ("Model Availability", test_model),
        ("Model Response", test_model_response),
        ("Python Dependencies", test_python_dependencies),
        ("GUI Imports", test_gui_imports)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"Testing {test_name}...")
        result = test_func()
        results.append((test_name, result))
        print()
    
    # Summary
    print("📊 Test Results Summary")
    print("=" * 30)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Language Teacher is ready to use!")
        print()
        print("To start the GUI:")
        print("  python gui_app.py")
        print("  or double-click start_language_teacher.bat")
    else:
        print("⚠️ Some tests failed. Please check the setup.")
        print("Run setup_complete.py to fix issues.")

if __name__ == "__main__":
    main()
