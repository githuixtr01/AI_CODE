"""
Simple LLM Router: Direct API calls without complex dependencies
"""
import os
import requests
import json

def llm_complete(prompt, provider="groq", model=None, **kwargs):
    """Simple LLM completion using direct API calls"""
    
    if provider == "groq":
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            return f"Error: GROQ_API_KEY not found in environment"
        
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model or "openai/gpt-oss-120b",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 1024)
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return f"Groq API Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Groq Error: {str(e)}"
    
    elif provider == "google":
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            return f"Error: GOOGLE_API_KEY not found in environment"
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                result = response.json()
                return result["candidates"][0]["content"]["parts"][0]["text"]
            else:
                return f"Google API Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Google Error: {str(e)}"
    
    else:
        return f"Unknown provider: {provider}"