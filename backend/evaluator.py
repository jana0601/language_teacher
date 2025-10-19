import requests
import json
from typing import List, Dict

class LanguageEvaluator:
    def __init__(self):
        """Initialize the language evaluator with Ollama API"""
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model = "llama3.2"  # Free Llama model
        
    def evaluate_conversation(self, conversation: List[Dict], language: str) -> Dict:
        """
        Evaluate a conversation and return detailed performance report
        
        Args:
            conversation: List of conversation messages
            language: Target language code
            
        Returns:
            Dictionary containing evaluation results
        """
        try:
            # Extract only user messages for evaluation
            user_messages = [msg['content'] for msg in conversation if msg['role'] == 'user']
            
            if not user_messages:
                return {
                    "overall_score": 0,
                    "mistakes": [],
                    "suggestions": ["No user messages found to evaluate"],
                    "summary": "No conversation to evaluate"
                }
            
            # Create evaluation prompt
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
            
            evaluation_prompt = f"""You are an expert language teacher evaluating a student's performance in {language_name}. 

Analyze the following student messages and provide a detailed evaluation:

Student messages:
{chr(10).join([f"{i+1}. {msg}" for i, msg in enumerate(user_messages)])}

Please provide your evaluation in the following JSON format:
{{
    "overall_score": <score from 0-100>,
    "mistakes": [
        {{
            "message": "<original incorrect text>",
            "correction": "<corrected version>",
            "explanation": "<brief explanation of the mistake>",
            "type": "<grammar/vocabulary/pronunciation/style>"
        }}
    ],
    "suggestions": [
        "<specific improvement suggestions>"
    ],
    "summary": "<overall performance summary>",
    "strengths": [
        "<things the student did well>"
    ],
    "areas_for_improvement": [
        "<areas that need more practice>"
    ]
}}

Focus on:
1. Grammar accuracy
2. Vocabulary usage
3. Sentence structure
4. Naturalness of expression
5. Communication effectiveness

Be constructive and encouraging while being specific about mistakes."""

            # Make API call to Ollama for evaluation
            prompt = f"""You are an expert language teacher. Always respond with valid JSON only.

{evaluation_prompt}"""
            
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "max_tokens": 1000
                }
            }
            
            response = requests.post(self.ollama_url, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            evaluation_text = result.get("response", "").strip()
            
            # Try to extract JSON from response (in case there's extra text)
            try:
                # Find JSON object in the response
                start_idx = evaluation_text.find('{')
                end_idx = evaluation_text.rfind('}') + 1
                json_text = evaluation_text[start_idx:end_idx]
                evaluation = json.loads(json_text)
            except (json.JSONDecodeError, ValueError):
                # Fallback if JSON parsing fails
                evaluation = {
                    "overall_score": 75,
                    "mistakes": [],
                    "suggestions": ["Unable to parse detailed evaluation. Please try again."],
                    "summary": "Evaluation completed but detailed analysis unavailable.",
                    "strengths": ["Student engaged in conversation"],
                    "areas_for_improvement": ["Continue practicing"]
                }
            
            # Ensure all required fields exist
            evaluation.setdefault("overall_score", 75)
            evaluation.setdefault("mistakes", [])
            evaluation.setdefault("suggestions", [])
            evaluation.setdefault("summary", "Evaluation completed")
            evaluation.setdefault("strengths", [])
            evaluation.setdefault("areas_for_improvement", [])
            
            return evaluation
            
        except Exception as e:
            # Fallback evaluation in case of error
            return {
                "overall_score": 0,
                "mistakes": [],
                "suggestions": [f"Evaluation error: {str(e)}"],
                "summary": "Unable to complete evaluation due to technical issues",
                "strengths": [],
                "areas_for_improvement": ["Please try again later"]
            }
