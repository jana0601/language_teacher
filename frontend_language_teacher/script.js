// Language Teacher Frontend JavaScript
class LanguageTeacher {
    constructor() {
        this.apiBase = 'http://localhost:5000/api';
        this.currentSession = null;
        this.selectedLanguage = null;
        this.languages = [];
        
        this.initializeElements();
        this.bindEvents();
        this.loadLanguages();
    }

    initializeElements() {
        // Screens
        this.languageSelectionScreen = document.getElementById('language-selection');
        this.chatInterfaceScreen = document.getElementById('chat-interface');
        
        // Language selection
        this.languageGrid = document.getElementById('language-grid');
        this.languageLoading = document.getElementById('language-loading');
        
        // Chat interface
        this.selectedLanguageSpan = document.getElementById('selected-language');
        this.changeLanguageBtn = document.getElementById('change-language');
        this.newConversationBtn = document.getElementById('new-conversation');
        this.evaluateBtn = document.getElementById('evaluate-btn');
        this.chatMessages = document.getElementById('chat-messages');
        this.messageInput = document.getElementById('message-input');
        this.sendBtn = document.getElementById('send-btn');
        
        // Evaluation modal
        this.evaluationModal = document.getElementById('evaluation-modal');
        this.closeEvaluationBtn = document.getElementById('close-evaluation');
        this.continueChatBtn = document.getElementById('continue-chat');
        this.newSessionBtn = document.getElementById('new-session');
        
        // Loading overlay
        this.loadingOverlay = document.getElementById('loading-overlay');
        this.loadingText = document.getElementById('loading-text');
    }

    bindEvents() {
        // Language selection
        this.changeLanguageBtn.addEventListener('click', () => this.showLanguageSelection());
        
        // Chat controls
        this.newConversationBtn.addEventListener('click', () => this.startNewConversation());
        this.evaluateBtn.addEventListener('click', () => this.requestEvaluation());
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        
        // Message input
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Evaluation modal
        this.closeEvaluationBtn.addEventListener('click', () => this.closeEvaluation());
        this.continueChatBtn.addEventListener('click', () => this.closeEvaluation());
        this.newSessionBtn.addEventListener('click', () => this.startNewSession());
        
        // Close modal on outside click
        this.evaluationModal.addEventListener('click', (e) => {
            if (e.target === this.evaluationModal) {
                this.closeEvaluation();
            }
        });
    }

    async loadLanguages() {
        try {
            const response = await fetch(`${this.apiBase}/languages`);
            this.languages = await response.json();
            this.renderLanguages();
        } catch (error) {
            console.error('Error loading languages:', error);
            this.languageLoading.textContent = 'Error loading languages. Please refresh the page.';
        }
    }

    renderLanguages() {
        this.languageLoading.style.display = 'none';
        this.languageGrid.innerHTML = '';
        
        this.languages.forEach(language => {
            const button = document.createElement('button');
            button.className = 'language-option';
            button.textContent = language.name;
            button.dataset.code = language.code;
            button.addEventListener('click', () => this.selectLanguage(language));
            this.languageGrid.appendChild(button);
        });
    }

    async selectLanguage(language) {
        this.selectedLanguage = language;
        
        // Visual feedback
        document.querySelectorAll('.language-option').forEach(btn => {
            btn.classList.remove('selected');
        });
        document.querySelector(`[data-code="${language.code}"]`).classList.add('selected');
        
        // Create new session
        await this.createNewSession();
        
        // Switch to chat interface
        this.showChatInterface();
    }

    async createNewSession() {
        try {
            const response = await fetch(`${this.apiBase}/session/new`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            const data = await response.json();
            this.currentSession = data.session_id;
        } catch (error) {
            console.error('Error creating session:', error);
            alert('Error creating new session. Please try again.');
        }
    }

    showLanguageSelection() {
        this.languageSelectionScreen.classList.add('active');
        this.chatInterfaceScreen.classList.remove('active');
    }

    showChatInterface() {
        this.languageSelectionScreen.classList.remove('active');
        this.chatInterfaceScreen.classList.add('active');
        this.selectedLanguageSpan.textContent = this.selectedLanguage.name;
        this.messageInput.focus();
    }

    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message || !this.currentSession) return;

        // Add user message to chat
        this.addMessageToChat(message, 'user');
        this.messageInput.value = '';

        // Show loading
        this.showLoading('Sending message...');

        try {
            const response = await fetch(`${this.apiBase}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    session_id: this.currentSession,
                    message: message,
                    language: this.selectedLanguage.code
                })
            });

            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }

            // Add AI response to chat
            this.addMessageToChat(data.response, 'assistant');
            
        } catch (error) {
            console.error('Error sending message:', error);
            this.addMessageToChat('Sorry, I encountered an error. Please try again.', 'assistant');
        } finally {
            this.hideLoading();
        }
    }

    addMessageToChat(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        const contentDiv = document.createElement('div');
        contentDiv.textContent = content;
        messageDiv.appendChild(contentDiv);
        
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = new Date().toLocaleTimeString();
        messageDiv.appendChild(timeDiv);
        
        this.chatMessages.appendChild(messageDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    async requestEvaluation() {
        if (!this.currentSession) {
            alert('No active session to evaluate.');
            return;
        }

        this.showLoading('Analyzing your conversation...');

        try {
            const response = await fetch(`${this.apiBase}/evaluate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    session_id: this.currentSession
                })
            });

            const evaluation = await response.json();
            
            if (evaluation.error) {
                throw new Error(evaluation.error);
            }

            this.displayEvaluation(evaluation);
            
        } catch (error) {
            console.error('Error getting evaluation:', error);
            alert('Error getting evaluation. Please try again.');
        } finally {
            this.hideLoading();
        }
    }

    displayEvaluation(evaluation) {
        // Update score
        document.getElementById('overall-score').textContent = evaluation.overall_score || 0;
        
        // Update summary
        document.getElementById('evaluation-summary').textContent = evaluation.summary || 'No summary available.';
        
        // Update strengths
        const strengthsList = document.getElementById('strengths-list');
        strengthsList.innerHTML = '';
        if (evaluation.strengths && evaluation.strengths.length > 0) {
            evaluation.strengths.forEach(strength => {
                const li = document.createElement('li');
                li.textContent = strength;
                strengthsList.appendChild(li);
            });
        } else {
            const li = document.createElement('li');
            li.textContent = 'No specific strengths identified.';
            li.style.fontStyle = 'italic';
            li.style.color = '#6c757d';
            strengthsList.appendChild(li);
        }
        
        // Update mistakes
        const mistakesList = document.getElementById('mistakes-list');
        mistakesList.innerHTML = '';
        if (evaluation.mistakes && evaluation.mistakes.length > 0) {
            evaluation.mistakes.forEach(mistake => {
                const mistakeDiv = document.createElement('div');
                mistakeDiv.className = 'mistake-item';
                
                mistakeDiv.innerHTML = `
                    <div class="mistake-original">❌ "${mistake.message}"</div>
                    <div class="mistake-correction">✅ "${mistake.correction}"</div>
                    <div class="mistake-explanation">${mistake.explanation || 'No explanation provided.'}</div>
                `;
                
                mistakesList.appendChild(mistakeDiv);
            });
        } else {
            const div = document.createElement('div');
            div.textContent = 'No mistakes found! Great job!';
            div.style.textAlign = 'center';
            div.style.color = '#38a169';
            div.style.fontStyle = 'italic';
            div.style.padding = '20px';
            mistakesList.appendChild(div);
        }
        
        // Update suggestions
        const suggestionsList = document.getElementById('suggestions-list');
        suggestionsList.innerHTML = '';
        if (evaluation.suggestions && evaluation.suggestions.length > 0) {
            evaluation.suggestions.forEach(suggestion => {
                const li = document.createElement('li');
                li.textContent = suggestion;
                suggestionsList.appendChild(li);
            });
        } else {
            const li = document.createElement('li');
            li.textContent = 'Keep practicing!';
            li.style.fontStyle = 'italic';
            li.style.color = '#6c757d';
            suggestionsList.appendChild(li);
        }
        
        // Update improvement areas
        const improvementList = document.getElementById('improvement-areas-list');
        improvementList.innerHTML = '';
        if (evaluation.areas_for_improvement && evaluation.areas_for_improvement.length > 0) {
            evaluation.areas_for_improvement.forEach(area => {
                const li = document.createElement('li');
                li.textContent = area;
                improvementList.appendChild(li);
            });
        } else {
            const li = document.createElement('li');
            li.textContent = 'Continue practicing to maintain your skills!';
            li.style.fontStyle = 'italic';
            li.style.color = '#6c757d';
            improvementList.appendChild(li);
        }
        
        // Show modal
        this.evaluationModal.classList.add('active');
    }

    closeEvaluation() {
        this.evaluationModal.classList.remove('active');
    }

    async startNewConversation() {
        if (confirm('Are you sure you want to start a new conversation? This will clear your current chat history.')) {
            await this.createNewSession();
            this.chatMessages.innerHTML = '';
            this.messageInput.focus();
        }
    }

    async startNewSession() {
        this.closeEvaluation();
        this.showLanguageSelection();
        this.chatMessages.innerHTML = '';
        this.currentSession = null;
        this.selectedLanguage = null;
    }

    showLoading(text = 'Loading...') {
        this.loadingText.textContent = text;
        this.loadingOverlay.classList.add('active');
    }

    hideLoading() {
        this.loadingOverlay.classList.remove('active');
    }
}

// Initialize the application when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new LanguageTeacher();
});
