import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import json
import sys
import os

# Add backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from chat_handler import ChatHandler
from evaluator import LanguageEvaluator
import uuid

class LanguageTeacherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🌍 Language Teacher - Practice & Learn")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize handlers
        self.chat_handler = ChatHandler()
        self.evaluator = LanguageEvaluator()
        
        # Session management
        self.current_session = None
        self.selected_language = None
        self.conversation_history = []
        
        # Available languages
        self.languages = [
            {"code": "en", "name": "English"},
            {"code": "es", "name": "Spanish"},
            {"code": "fr", "name": "French"},
            {"code": "de", "name": "German"},
            {"code": "it", "name": "Italian"},
            {"code": "pt", "name": "Portuguese"},
            {"code": "ru", "name": "Russian"},
            {"code": "ja", "name": "Japanese"},
            {"code": "ko", "name": "Korean"},
            {"code": "zh", "name": "Chinese"},
        ]
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the main user interface"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="🌍 Language Teacher", 
                              font=('Arial', 24, 'bold'), 
                              bg='#f0f0f0', fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        subtitle_label = tk.Label(main_frame, text="Practice conversations and get detailed feedback", 
                                font=('Arial', 12), 
                                bg='#f0f0f0', fg='#7f8c8d')
        subtitle_label.pack(pady=(0, 30))
        
        # Control panel
        self.setup_control_panel(main_frame)
        
        # Chat area
        self.setup_chat_area(main_frame)
        
        # Input area
        self.setup_input_area(main_frame)
        
        # Evaluation area
        self.setup_evaluation_area(main_frame)
        
    def setup_control_panel(self, parent):
        """Setup the control panel with language selection and buttons"""
        control_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=1)
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Language selection
        lang_frame = tk.Frame(control_frame, bg='white')
        lang_frame.pack(side=tk.LEFT, padx=20, pady=15)
        
        tk.Label(lang_frame, text="Target Language:", 
                font=('Arial', 12, 'bold'), bg='white').pack(side=tk.LEFT)
        
        self.language_var = tk.StringVar()
        self.language_combo = ttk.Combobox(lang_frame, textvariable=self.language_var,
                                         values=[lang['name'] for lang in self.languages],
                                         state='readonly', width=15)
        self.language_combo.pack(side=tk.LEFT, padx=(10, 0))
        self.language_combo.bind('<<ComboboxSelected>>', self.on_language_selected)
        
        # Control buttons
        button_frame = tk.Frame(control_frame, bg='white')
        button_frame.pack(side=tk.RIGHT, padx=20, pady=15)
        
        self.new_session_btn = tk.Button(button_frame, text="🆕 New Session", 
                                       command=self.new_session,
                                       bg='#3498db', fg='white', font=('Arial', 10, 'bold'),
                                       relief=tk.FLAT, padx=15, pady=5)
        self.new_session_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.evaluate_btn = tk.Button(button_frame, text="📊 Get Evaluation", 
                                    command=self.request_evaluation,
                                    bg='#e74c3c', fg='white', font=('Arial', 10, 'bold'),
                                    relief=tk.FLAT, padx=15, pady=5, state=tk.DISABLED)
        self.evaluate_btn.pack(side=tk.LEFT)
        
    def setup_chat_area(self, parent):
        """Setup the chat conversation area"""
        chat_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=1)
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Chat header
        chat_header = tk.Frame(chat_frame, bg='#34495e', height=40)
        chat_header.pack(fill=tk.X)
        chat_header.pack_propagate(False)
        
        self.chat_title = tk.Label(chat_header, text="💬 Conversation", 
                                 font=('Arial', 14, 'bold'), 
                                 bg='#34495e', fg='white')
        self.chat_title.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Chat messages area
        self.chat_text = scrolledtext.ScrolledText(chat_frame, 
                                                 font=('Arial', 11),
                                                 bg='#f8f9fa', fg='#2c3e50',
                                                 wrap=tk.WORD, state=tk.DISABLED)
        self.chat_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Configure text tags for styling
        self.chat_text.tag_configure("user", background="#3498db", foreground="white", 
                                    relief=tk.RAISED, borderwidth=1)
        self.chat_text.tag_configure("assistant", background="#ecf0f1", foreground="#2c3e50",
                                    relief=tk.RAISED, borderwidth=1)
        self.chat_text.tag_configure("timestamp", foreground="#7f8c8d", font=('Arial', 9))
        
    def setup_input_area(self, parent):
        """Setup the message input area"""
        input_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=1)
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Input field
        input_inner = tk.Frame(input_frame, bg='white')
        input_inner.pack(fill=tk.X, padx=20, pady=15)
        
        self.message_var = tk.StringVar()
        self.message_entry = tk.Entry(input_inner, textvariable=self.message_var,
                                     font=('Arial', 12), relief=tk.FLAT, bd=1)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.message_entry.bind('<Return>', self.send_message)
        
        self.send_btn = tk.Button(input_inner, text="📤 Send", 
                                command=self.send_message,
                                bg='#27ae60', fg='white', font=('Arial', 10, 'bold'),
                                relief=tk.FLAT, padx=20, pady=5, state=tk.DISABLED)
        self.send_btn.pack(side=tk.RIGHT)
        
        # Status label
        self.status_label = tk.Label(input_frame, text="Select a language to start chatting", 
                                   font=('Arial', 10), bg='white', fg='#7f8c8d')
        self.status_label.pack(pady=(0, 10))
        
    def setup_evaluation_area(self, parent):
        """Setup the evaluation results area"""
        eval_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=1)
        eval_frame.pack(fill=tk.BOTH, expand=True)
        
        # Evaluation header
        eval_header = tk.Frame(eval_frame, bg='#e74c3c', height=40)
        eval_header.pack(fill=tk.X)
        eval_header.pack_propagate(False)
        
        tk.Label(eval_header, text="📊 Performance Evaluation", 
                font=('Arial', 14, 'bold'), 
                bg='#e74c3c', fg='white').pack(side=tk.LEFT, padx=20, pady=10)
        
        # Evaluation content
        self.eval_text = scrolledtext.ScrolledText(eval_frame, 
                                                  font=('Arial', 10),
                                                  bg='#f8f9fa', fg='#2c3e50',
                                                  wrap=tk.WORD, state=tk.DISABLED)
        self.eval_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Configure evaluation text tags
        self.eval_text.tag_configure("score", foreground="#e74c3c", font=('Arial', 16, 'bold'))
        self.eval_text.tag_configure("heading", foreground="#2c3e50", font=('Arial', 12, 'bold'))
        self.eval_text.tag_configure("mistake", foreground="#e74c3c", font=('Arial', 10, 'bold'))
        self.eval_text.tag_configure("correction", foreground="#27ae60", font=('Arial', 10, 'bold'))
        self.eval_text.tag_configure("suggestion", foreground="#3498db", font=('Arial', 10))
        
    def on_language_selected(self, event):
        """Handle language selection"""
        selected_name = self.language_var.get()
        self.selected_language = next(lang for lang in self.languages if lang['name'] == selected_name)
        
        self.status_label.config(text=f"Selected: {selected_name}. Click 'New Session' to start chatting.")
        self.new_session_btn.config(state=tk.NORMAL)
        
    def new_session(self):
        """Start a new conversation session"""
        if not self.selected_language:
            messagebox.showwarning("Warning", "Please select a language first!")
            return
            
        self.current_session = str(uuid.uuid4())
        self.conversation_history = []
        
        # Clear chat
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.delete(1.0, tk.END)
        self.chat_text.config(state=tk.DISABLED)
        
        # Update UI
        self.chat_title.config(text=f"💬 Conversation in {self.selected_language['name']}")
        self.status_label.config(text=f"New session started! Start chatting in {self.selected_language['name']}")
        self.send_btn.config(state=tk.NORMAL)
        self.evaluate_btn.config(state=tk.NORMAL)
        self.message_entry.focus()
        
        # Add welcome message
        self.add_message_to_chat("Hello! I'm here to help you practice. Let's start a conversation!", "assistant")
        
    def send_message(self, event=None):
        """Send a message and get AI response"""
        message = self.message_var.get().strip()
        if not message or not self.current_session:
            return
            
        # Add user message to chat
        self.add_message_to_chat(message, "user")
        self.message_var.set("")
        
        # Disable input while processing
        self.send_btn.config(state=tk.DISABLED)
        self.message_entry.config(state=tk.DISABLED)
        self.status_label.config(text="AI is thinking...")
        
        # Add user message to conversation history
        self.conversation_history.append({"role": "user", "content": message})
        
        # Get AI response in a separate thread
        threading.Thread(target=self.get_ai_response, daemon=True).start()
        
    def get_ai_response(self):
        """Get AI response (runs in separate thread)"""
        try:
            ai_response = self.chat_handler.get_response(
                self.conversation_history[-1]["content"],
                self.selected_language["code"],
                self.conversation_history
            )
            
            # Add AI response to conversation history
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            # Update UI in main thread
            self.root.after(0, lambda: self.add_message_to_chat(ai_response, "assistant"))
            self.root.after(0, self.enable_input)
            
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            self.conversation_history.append({"role": "assistant", "content": error_msg})
            self.root.after(0, lambda: self.add_message_to_chat(error_msg, "assistant"))
            self.root.after(0, self.enable_input)
            
    def enable_input(self):
        """Re-enable input after AI response"""
        self.send_btn.config(state=tk.NORMAL)
        self.message_entry.config(state=tk.NORMAL)
        self.status_label.config(text=f"Ready to chat in {self.selected_language['name']}")
        self.message_entry.focus()
        
    def add_message_to_chat(self, message, sender):
        """Add a message to the chat display"""
        self.chat_text.config(state=tk.NORMAL)
        
        # Add timestamp
        timestamp = tk.datetime.now().strftime("%H:%M")
        self.chat_text.insert(tk.END, f"[{timestamp}] ", "timestamp")
        
        # Add message with appropriate styling
        if sender == "user":
            self.chat_text.insert(tk.END, f"You: {message}\n\n", "user")
        else:
            self.chat_text.insert(tk.END, f"AI: {message}\n\n", "assistant")
            
        self.chat_text.config(state=tk.DISABLED)
        self.chat_text.see(tk.END)
        
    def request_evaluation(self):
        """Request evaluation of the conversation"""
        if not self.conversation_history or not self.current_session:
            messagebox.showwarning("Warning", "No conversation to evaluate!")
            return
            
        # Disable evaluate button
        self.evaluate_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Analyzing your conversation...")
        
        # Run evaluation in separate thread
        threading.Thread(target=self.run_evaluation, daemon=True).start()
        
    def run_evaluation(self):
        """Run evaluation (runs in separate thread)"""
        try:
            evaluation = self.evaluator.evaluate_conversation(
                self.conversation_history,
                self.selected_language["code"]
            )
            
            # Update UI in main thread
            self.root.after(0, lambda: self.display_evaluation(evaluation))
            
        except Exception as e:
            error_msg = f"Evaluation error: {str(e)}"
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
            self.root.after(0, lambda: self.evaluate_btn.config(state=tk.NORMAL))
            
    def display_evaluation(self, evaluation):
        """Display evaluation results"""
        self.eval_text.config(state=tk.NORMAL)
        self.eval_text.delete(1.0, tk.END)
        
        # Overall score
        score = evaluation.get("overall_score", 0)
        self.eval_text.insert(tk.END, f"Overall Score: {score}/100\n", "score")
        self.eval_text.insert(tk.END, "\n")
        
        # Summary
        summary = evaluation.get("summary", "No summary available.")
        self.eval_text.insert(tk.END, "📝 Summary:\n", "heading")
        self.eval_text.insert(tk.END, f"{summary}\n\n")
        
        # Strengths
        strengths = evaluation.get("strengths", [])
        if strengths:
            self.eval_text.insert(tk.END, "✅ Strengths:\n", "heading")
            for strength in strengths:
                self.eval_text.insert(tk.END, f"• {strength}\n")
            self.eval_text.insert(tk.END, "\n")
        
        # Mistakes
        mistakes = evaluation.get("mistakes", [])
        if mistakes:
            self.eval_text.insert(tk.END, "❌ Mistakes & Corrections:\n", "heading")
            for mistake in mistakes:
                self.eval_text.insert(tk.END, f"• ", "mistake")
                self.eval_text.insert(tk.END, f'"{mistake.get("message", "")}"', "mistake")
                self.eval_text.insert(tk.END, " → ", "mistake")
                self.eval_text.insert(tk.END, f'"{mistake.get("correction", "")}"', "correction")
                self.eval_text.insert(tk.END, f"\n  {mistake.get('explanation', '')}\n")
            self.eval_text.insert(tk.END, "\n")
        else:
            self.eval_text.insert(tk.END, "🎉 No mistakes found! Great job!\n\n")
        
        # Suggestions
        suggestions = evaluation.get("suggestions", [])
        if suggestions:
            self.eval_text.insert(tk.END, "💡 Suggestions:\n", "heading")
            for suggestion in suggestions:
                self.eval_text.insert(tk.END, f"• {suggestion}\n", "suggestion")
            self.eval_text.insert(tk.END, "\n")
        
        # Areas for improvement
        improvements = evaluation.get("areas_for_improvement", [])
        if improvements:
            self.eval_text.insert(tk.END, "🎯 Areas for Improvement:\n", "heading")
            for area in improvements:
                self.eval_text.insert(tk.END, f"• {area}\n")
        
        self.eval_text.config(state=tk.DISABLED)
        self.evaluate_btn.config(state=tk.NORMAL)
        self.status_label.config(text=f"Evaluation complete! Score: {score}/100")

def main():
    """Main function to run the GUI application"""
    root = tk.Tk()
    app = LanguageTeacherGUI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
