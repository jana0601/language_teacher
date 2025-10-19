#!/usr/bin/env python3
"""
Language Teacher Web Server
Simple HTTP server to serve the web application
"""

import http.server
import socketserver
import webbrowser
import os
import sys
import threading
import time

# Add backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from main import app as flask_app

class WebHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler to serve HTML files"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(__file__), **kwargs)
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def start_flask_server():
    """Start the Flask backend server"""
    print("Starting Flask backend server...")
    try:
        flask_app.run(host='localhost', port=5000, debug=False, use_reloader=False)
    except Exception as e:
        print(f"Error starting Flask server: {e}")

def start_web_server():
    """Start the web server"""
    PORT = 8000
    
    print(f"Starting web server on port {PORT}...")
    
    with socketserver.TCPServer(("", PORT), WebHandler) as httpd:
        print(f"Web server running at http://localhost:{PORT}")
        print("Opening browser...")
        
        # Open browser after a short delay
        def open_browser():
            time.sleep(1)
            webbrowser.open(f'http://localhost:{PORT}/web_app.html')
        
        threading.Thread(target=open_browser, daemon=True).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down web server...")
            httpd.shutdown()

def main():
    """Main function"""
    print("🌍 Language Teacher Web Application")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists('web_app.html'):
        print("ERROR: web_app.html not found!")
        print("Please run this script from the language_teacher directory")
        return
    
    # Start Flask server in background
    flask_thread = threading.Thread(target=start_flask_server, daemon=True)
    flask_thread.start()
    
    # Wait a moment for Flask to start
    time.sleep(2)
    
    # Start web server
    start_web_server()

if __name__ == "__main__":
    main()
