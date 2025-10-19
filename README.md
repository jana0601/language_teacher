# Language Teacher Application

A web-based language learning application that allows students to practice conversations in their target language and receive detailed evaluations with specific mistake corrections using free open-source AI models.
![Interface Screenshot](https://github.com/jana0601/language_teacher/blob/main/interface.jpg?raw=true)

## Features

- **Multi-language Support**: Practice conversations in 10 different languages
- **Real-time Chat**: Interactive conversations with AI in your target language
- **Detailed Evaluation**: Get comprehensive feedback on your language performance
- **Mistake Analysis**: Specific corrections and explanations for errors
- **Progress Tracking**: See your strengths and areas for improvement
- **Two Interfaces**: Web-based and Desktop GUI versions available

## Supported Languages

- English
- Spanish
- French
- German
- Italian
- Portuguese
- Russian
- Japanese
- Korean
- Chinese

## Quick Start

### Prerequisites

- Python 3.11+
- Ollama (for free AI models) - Download from https://ollama.ai
- Docker (optional)

### Option 1: Docker (Recommended)

1. **Install Ollama**: Download and install from https://ollama.ai
2. **Pull the Llama model**: Run `ollama pull llama3.2` in your terminal
3. **Start Ollama**: Run `ollama serve` (it will run on localhost:11434)
4. Clone or download this project
5. Run with Docker Compose:
   ```bash
   docker-compose up -d
   ```
6. Open your browser to `http://localhost`

### Option 2: Manual Setup

1. **Install Ollama**: Download and install from https://ollama.ai
2. **Pull the Llama model**: Run `ollama pull llama3.2` in your terminal
3. **Start Ollama**: Run `ollama serve` (it will run on localhost:11434)
4. **Backend Setup**:
   ```bash
   cd backend
   pip install -r requirements.txt
   python main.py
   ```

5. **Frontend Setup**:
   ```bash
   cd frontend
   # Serve the files using any web server, or open index.html directly
   python -m http.server 8000
   ```

6. Open your browser to `http://localhost:8000` (or wherever you're serving the frontend)

### Option 3: Desktop GUI (Easiest)

1. **Install Ollama**: Download and install from https://ollama.ai
2. **Run Complete Setup**: 
   - **Windows**: Double-click `setup_complete.bat`
   - **Linux/Mac**: Run `python setup_complete.py`
3. **Verify Setup**: Run `python verify_setup.py` (optional)
4. **Start GUI**: Run `python gui_app.py` or double-click `start_language_teacher.bat`

### Option 4: Automated Setup (Recommended)

1. **Install Ollama**: Download from https://ollama.ai
2. **Run Setup Script**: 
   - **Windows**: `setup_complete.bat`
   - **Linux/Mac**: `python setup_complete.py`
3. **The script will automatically**:
   - Start Ollama service
   - Download llama3.2 model
   - Install Python dependencies
   - Test everything
   - Create startup script
4. **Start using**: `python gui_app.py`

## Usage

### Web Interface
1. **Select Language**: Choose your target language from the grid
2. **Start Chatting**: Type messages in your target language
3. **Get Feedback**: Click "Get Evaluation" to receive detailed analysis
4. **Review Results**: See your score, mistakes, corrections, and suggestions
5. **Continue Learning**: Start new conversations or continue practicing

### Desktop GUI Interface
1. **Launch**: Run `run_gui.bat` (Windows) or `python run_gui.py` (Linux/Mac)
2. **Select Language**: Choose from the dropdown menu
3. **New Session**: Click "New Session" to start chatting
4. **Chat**: Type messages and press Enter to send
5. **Evaluate**: Click "Get Evaluation" to see detailed feedback
6. **Review**: Check the evaluation panel for scores, mistakes, and suggestions

## API Endpoints

- `GET /api/languages` - Get available languages
- `POST /api/session/new` - Create new conversation session
- `POST /api/chat` - Send message and get AI response
- `POST /api/evaluate` - Get performance evaluation
- `POST /api/session/{id}/clear` - Clear conversation history

## Configuration

### Environment Variables

- `OLLAMA_URL`: Ollama server URL (default: http://localhost:11434)
- `OLLAMA_MODEL`: Model to use (default: llama3.2)
- `FLASK_ENV`: Flask environment (development/production)
- `FLASK_DEBUG`: Enable debug mode (True/False)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 5000)

## Development

### Project Structure

```
language_teacher/
├── backend/
│   ├── main.py              # Flask server
│   ├── chat_handler.py      # Chat conversation logic
│   ├── evaluator.py         # Language evaluation engine
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile          # Container configuration
├── frontend/
│   ├── index.html          # Main UI
│   ├── style.css           # Styling
│   └── script.js           # Client-side logic
├── docker-compose.yml      # Multi-container orchestration
├── .env.example           # Environment variables template
└── README.md              # This file
```

### Adding New Languages

To add support for new languages:

1. Update the `languages` list in `backend/main.py`
2. Add language-specific prompts in `backend/chat_handler.py`
3. Update fallback responses in `backend/chat_handler.py`

## Troubleshooting

### Common Issues

1. **"Error loading languages"**: Check if the backend is running on port 5000
2. **"Error sending message"**: Verify Ollama is running (`ollama serve`) and llama3.2 model is installed (`ollama pull llama3.2`)
3. **CORS errors**: Make sure Flask-CORS is installed and configured
4. **Evaluation fails**: Check if Ollama is running and has enough memory for the model
5. **Connection refused**: Ensure Ollama is running on localhost:11434

### Logs

- Backend logs: Check the terminal where you ran `python main.py`
- Docker logs: `docker-compose logs backend`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Open an issue on the project repository
