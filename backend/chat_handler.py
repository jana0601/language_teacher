import requests
import json
from typing import List, Dict

class ChatHandler:
    def __init__(self):
        """Initialize the chat handler with Ollama API"""
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model = "llama3.2"  # Free Llama model
        
    def get_response(self, user_message: str, language: str, conversation_history: List[Dict]) -> str:
        """
        Get AI response in the target language
        
        Args:
            user_message: The user's message
            language: Target language code (e.g., 'en', 'es', 'fr')
            conversation_history: Previous conversation messages
            
        Returns:
            AI response in the target language
        """
        try:
            # Create system prompt based on target language
            language_names = {
                'en': 'English',
                'es': 'Spanish', 
                'fr': 'French',
                'de': 'German',
                'it': 'Italian',
                'pt': 'Portuguese',
                'ru': 'Russian',
                'ja': 'Japanese',
                'ko': 'Korean',
                'zh': 'Chinese'
            }
            
            language_name = language_names.get(language, 'English')
            
            system_prompt = f"""You are a helpful language learning assistant. You are having a conversation with a student who is learning {language_name}.

IMPORTANT RULES:
1. You MUST respond ONLY in {language_name}. Never use any other language.
2. Keep your responses natural and conversational.
3. Ask follow-up questions to keep the conversation flowing.
4. Be encouraging and supportive.
5. Keep responses concise but engaging.
6. Adapt to the student's level - if they make mistakes, don't correct them directly in your response, just continue the conversation naturally.

Start the conversation by greeting the student in {language_name} and asking them about their day or interests."""

            # Prepare messages for OpenAI API
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add conversation history (limit to last 10 exchanges to avoid token limits)
            recent_history = conversation_history[-20:]  # Last 10 exchanges (20 messages)
            messages.extend(recent_history)
            
            # Prepare prompt for Ollama
            prompt = self._format_prompt_for_ollama(messages)
            
            # Make API call to Ollama
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "max_tokens": 200
                }
            }
            
            response = requests.post(self.ollama_url, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "").strip()
            
        except Exception as e:
            # Fallback response in case of API error
            fallback_responses = {
                'en': "I'm sorry, I'm having trouble responding right now. Could you try again?",
                'es': "Lo siento, tengo problemas para responder ahora. ¿Podrías intentar de nuevo?",
                'fr': "Je suis désolé, j'ai des difficultés à répondre maintenant. Pourriez-vous réessayer?",
                'de': "Es tut mir leid, ich habe gerade Probleme beim Antworten. Könnten Sie es nochmal versuchen?",
                'it': "Mi dispiace, ho problemi a rispondere ora. Potresti riprovare?",
                'pt': "Desculpe, estou tendo problemas para responder agora. Você poderia tentar novamente?",
                'ru': "Извините, у меня проблемы с ответом сейчас. Не могли бы вы попробовать еще раз?",
                'ja': "申し訳ありませんが、今は返答に問題があります。もう一度お試しいただけますか？",
                'ko': "죄송합니다. 지금 응답에 문제가 있습니다. 다시 시도해 주시겠습니까?",
                'zh': "抱歉，我现在回复有问题。您能再试一次吗？"
            }
            return fallback_responses.get(language, fallback_responses['en'])
    
    def _format_prompt_for_ollama(self, messages: List[Dict]) -> str:
        """Format messages for Ollama API"""
        prompt_parts = []
        
        for message in messages:
            if message["role"] == "system":
                prompt_parts.append(f"System: {message['content']}")
            elif message["role"] == "user":
                prompt_parts.append(f"Human: {message['content']}")
            elif message["role"] == "assistant":
                prompt_parts.append(f"Assistant: {message['content']}")
        
        prompt_parts.append("Assistant:")
        return "\n\n".join(prompt_parts)
