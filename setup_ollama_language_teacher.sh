#!/bin/bash
# Setup script for Language Teacher with Ollama

echo "🌍 Language Teacher Setup Script"
echo "================================"

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed!"
    echo "Please install Ollama from: https://ollama.ai"
    echo "Then run this script again."
    exit 1
fi

echo "✅ Ollama is installed"

# Check if llama3.2 model is available
if ! ollama list | grep -q "llama3.2"; then
    echo "📥 Downloading llama3.2 model (this may take a few minutes)..."
    ollama pull llama3.2
    if [ $? -eq 0 ]; then
        echo "✅ llama3.2 model downloaded successfully"
    else
        echo "❌ Failed to download llama3.2 model"
        exit 1
    fi
else
    echo "✅ llama3.2 model is already available"
fi

# Start Ollama server
echo "🚀 Starting Ollama server..."
ollama serve &
OLLAMA_PID=$!

# Wait a moment for server to start
sleep 3

# Check if server is running
if curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "✅ Ollama server is running on localhost:11434"
else
    echo "❌ Failed to start Ollama server"
    kill $OLLAMA_PID 2>/dev/null
    exit 1
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Install Python dependencies: pip install -r backend/requirements.txt"
echo "2. Start the backend: cd backend && python main.py"
echo "3. Open frontend/index.html in your browser"
echo ""
echo "Ollama server is running in the background (PID: $OLLAMA_PID)"
echo "To stop Ollama: kill $OLLAMA_PID"
