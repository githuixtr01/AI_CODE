#!/usr/bin/env python3
"""
🔑 API Quota Manager with Automatic Fallback
Handles API quota exhaustion and automatically requests new API keys
"""
import json
import time
import random
import os
from groq import Groq
import google.generativeai as genai

class APIQuotaManager:
    def __init__(self, config_path="config/apis.json"):
        self.config_path = config_path
        self.apis = self.load_apis()
        self.api_usage = {}
        self.failed_apis = set()
        self.current_groq_index = 0
        self.current_google_index = 0
        
    def load_apis(self):
        """Load API configuration"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("[APIManager] ⚠️ API config not found, creating template...")
            return self.create_template_config()
    
    def create_template_config(self):
        """Create template API configuration"""
        template = {
            "groq": {
                "api_keys": [],
                "model": "openai/gpt-oss-120b",
                "primary": True
            },
            "google": {
                "api_keys": [],
                "model": "gemini-pro", 
                "backup": True
            }
        }
        
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(template, f, indent=2)
        
        return template
    
    def add_api_key(self, provider, api_key):
        """Add new API key to configuration"""
        if provider not in self.apis:
            self.apis[provider] = {"api_keys": [], "model": "default"}
        
        if "api_keys" not in self.apis[provider]:
            self.apis[provider]["api_keys"] = []
        
        if api_key not in self.apis[provider]["api_keys"]:
            self.apis[provider]["api_keys"].append(api_key)
            self.save_apis()
            print(f"[APIManager] ✅ Added new {provider} API key")
            return True
        else:
            print(f"[APIManager] ⚠️ {provider} API key already exists")
            return False
    
    def save_apis(self):
        """Save API configuration to file"""
        with open(self.config_path, 'w') as f:
            json.dump(self.apis, f, indent=2)
    
    def get_working_groq_client(self):
        """Get working Groq client with automatic fallback"""
        groq_keys = self.apis.get("groq", {}).get("api_keys", [])
        
        if not groq_keys:
            print("[APIManager] ❌ No Groq API keys available")
            return None
        
        # Try each Groq key
        for i in range(len(groq_keys)):
            key_index = (self.current_groq_index + i) % len(groq_keys)
            api_key = groq_keys[key_index]
            
            if api_key in self.failed_apis:
                continue
            
            try:
                client = Groq(api_key=api_key)
                # Test the client with a simple request
                response = client.chat.completions.create(
                    model=self.apis["groq"].get("model", "openai/gpt-oss-120b"),
                    messages=[{"role": "user", "content": "Test"}],
                    max_tokens=10
                )
                
                self.current_groq_index = key_index
                print(f"[APIManager] ✅ Using Groq API key #{key_index + 1}")
                return client
                
            except Exception as e:
                print(f"[APIManager] ❌ Groq key #{key_index + 1} failed: {e}")
                self.failed_apis.add(api_key)
                
                # Check if quota exceeded
                if "quota" in str(e).lower() or "limit" in str(e).lower():
                    print(f"[APIManager] ⚠️ Groq API quota exhausted for key #{key_index + 1}")
        
        # All keys failed, request new one
        print("[APIManager] 🔑 All Groq API keys exhausted, requesting new key...")
        return self.request_new_groq_key()
    
    def get_working_google_client(self):
        """Get working Google Gemini client with automatic fallback"""
        google_keys = self.apis.get("google", {}).get("api_keys", [])
        
        if not google_keys:
            print("[APIManager] ❌ No Google API keys available")
            return None
        
        # Try each Google key
        for i in range(len(google_keys)):
            key_index = (self.current_google_index + i) % len(google_keys)
            api_key = google_keys[key_index]
            
            if api_key in self.failed_apis:
                continue
            
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(self.apis["google"].get("model", "gemini-pro"))
                
                # Test the client
                response = model.generate_content("Test")
                
                self.current_google_index = key_index
                print(f"[APIManager] ✅ Using Google API key #{key_index + 1}")
                return model
                
            except Exception as e:
                print(f"[APIManager] ❌ Google key #{key_index + 1} failed: {e}")
                self.failed_apis.add(api_key)
                
                if "quota" in str(e).lower() or "limit" in str(e).lower():
                    print(f"[APIManager] ⚠️ Google API quota exhausted for key #{key_index + 1}")
        
        # All keys failed, request new one
        print("[APIManager] 🔑 All Google API keys exhausted, requesting new key...")
        return self.request_new_google_key()
    
    def request_new_groq_key(self):
        """Request new Groq API key from user"""
        print("\n" + "="*60)
        print("🔑 GROQ API KEY REQUIRED")
        print("="*60)
        print("Your Groq API quota has been exhausted.")
        print("Please obtain a new API key from: https://console.groq.com/keys")
        print("="*60)
        
        # Auto-prompt for new key
        try:
            new_key = input("Enter new Groq API key (or press Enter to skip): ").strip()
            if new_key:
                if self.add_api_key("groq", new_key):
                    # Reset failed APIs for this provider
                    groq_keys = self.apis.get("groq", {}).get("api_keys", [])
                    for key in groq_keys:
                        self.failed_apis.discard(key)
                    return self.get_working_groq_client()
            else:
                print("[APIManager] ⚠️ Skipping Groq API, will try Google Gemini...")
                return None
        except KeyboardInterrupt:
            print("\n[APIManager] ⚠️ API key input cancelled")
            return None
    
    def request_new_google_key(self):
        """Request new Google API key from user"""
        print("\n" + "="*60)
        print("🔑 GOOGLE GEMINI API KEY REQUIRED")
        print("="*60)
        print("Your Google Gemini API quota has been exhausted.")
        print("Please obtain a new API key from: https://aistudio.google.com/app/apikey")
        print("="*60)
        
        try:
            new_key = input("Enter new Google Gemini API key (or press Enter to skip): ").strip()
            if new_key:
                if self.add_api_key("google", new_key):
                    # Reset failed APIs for this provider
                    google_keys = self.apis.get("google", {}).get("api_keys", [])
                    for key in google_keys:
                        self.failed_apis.discard(key)
                    return self.get_working_google_client()
            else:
                print("[APIManager] ⚠️ No Google API key provided")
                return None
        except KeyboardInterrupt:
            print("\n[APIManager] ⚠️ API key input cancelled")
            return None
    
    def get_best_client(self):
        """Get the best available AI client with automatic fallback"""
        # Try Groq first (faster)
        groq_client = self.get_working_groq_client()
        if groq_client:
            return ("groq", groq_client)
        
        # Fallback to Google Gemini
        google_client = self.get_working_google_client()
        if google_client:
            return ("google", google_client)
        
        print("[APIManager] ❌ No working API clients available")
        return (None, None)
    
    def make_completion(self, prompt, max_tokens=1000):
        """Make AI completion with automatic provider fallback"""
        provider, client = self.get_best_client()
        
        if not client:
            return "Error: No working API clients available"
        
        try:
            if provider == "groq":
                response = client.chat.completions.create(
                    model=self.apis["groq"].get("model", "openai/gpt-oss-120b"),
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=0.7
                )
                return response.choices[0].message.content
            
            elif provider == "google":
                response = client.generate_content(prompt)
                return response.text
                
        except Exception as e:
            print(f"[APIManager] ❌ Completion failed: {e}")
            # Mark this API as failed and try again
            if provider == "groq":
                current_key = self.apis["groq"]["api_keys"][self.current_groq_index]
                self.failed_apis.add(current_key)
            elif provider == "google":
                current_key = self.apis["google"]["api_keys"][self.current_google_index]
                self.failed_apis.add(current_key)
            
            # Recursive retry with different provider
            return self.make_completion(prompt, max_tokens)
    
    def get_api_status(self):
        """Get status of all API keys"""
        status = {
            "groq": {
                "total_keys": len(self.apis.get("groq", {}).get("api_keys", [])),
                "working_keys": 0,
                "failed_keys": 0
            },
            "google": {
                "total_keys": len(self.apis.get("google", {}).get("api_keys", [])),
                "working_keys": 0,
                "failed_keys": 0
            }
        }
        
        # Count working vs failed keys
        for provider in ["groq", "google"]:
            keys = self.apis.get(provider, {}).get("api_keys", [])
            for key in keys:
                if key in self.failed_apis:
                    status[provider]["failed_keys"] += 1
                else:
                    status[provider]["working_keys"] += 1
        
        return status