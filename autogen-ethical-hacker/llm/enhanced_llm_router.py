#!/usr/bin/env python3
"""
🔄 Enhanced LLM Router with Self-Healing Capabilities
Provides robust API failover, retry mechanisms, and automatic recovery
"""

import os
import time
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

class EnhancedLLMRouter:
    """
    Self-healing LLM router with automatic failover and recovery
    """
    
    def __init__(self):
        self.groq_api_key = os.environ.get("GROQ_API_KEY")
        self.google_api_key = os.environ.get("GOOGLE_API_KEY") 
        
        # Provider status tracking
        self.provider_status = {
            'groq': {'healthy': True, 'last_success': None, 'consecutive_failures': 0, 'total_requests': 0},
            'google': {'healthy': True, 'last_success': None, 'consecutive_failures': 0, 'total_requests': 0}
        }
        
        # Circuit breaker settings
        self.circuit_breaker = {
            'failure_threshold': 3,  # Failures before marking unhealthy
            'recovery_timeout': 300,  # Seconds before attempting recovery
            'max_retries': 3
        }
        
        # Health check settings
        self.health_check_interval = 600  # 10 minutes
        self.last_health_check = None
        
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging for LLM operations"""
        self.logger = logging.getLogger('EnhancedLLMRouter')
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def _call_groq_api(self, prompt: str, **kwargs) -> str:
        """Call Groq API with error handling"""
        try:
            import groq
            
            if not self.groq_api_key:
                raise Exception("GROQ_API_KEY not found in environment")
            
            client = groq.Groq(api_key=self.groq_api_key)
            
            # Use the specified model or default
            model = kwargs.get("model", "openai/gpt-oss-120b")
            max_tokens = kwargs.get("max_tokens", 1024)
            temperature = kwargs.get("temperature", 0.7)
            
            completion = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            result = completion.choices[0].message.content
            self._record_success('groq')
            return result
            
        except Exception as e:
            self._record_failure('groq', str(e))
            raise e
    
    def _call_google_api(self, prompt: str, **kwargs) -> str:
        """Call Google Gemini API with error handling"""
        try:
            import google.generativeai as genai
            
            if not self.google_api_key:
                raise Exception("GOOGLE_API_KEY not found in environment")
            
            genai.configure(api_key=self.google_api_key)
            
            # Use the specified model or default
            model_name = kwargs.get("model", "gemini-1.5-pro")
            model = genai.GenerativeModel(model_name)
            
            # Configure generation parameters
            generation_config = {
                "temperature": kwargs.get("temperature", 0.7),
                "max_output_tokens": kwargs.get("max_tokens", 1024),
            }
            
            response = model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            result = response.text
            self._record_success('google')
            return result
            
        except Exception as e:
            self._record_failure('google', str(e))
            raise e
    
    def _record_success(self, provider: str):
        """Record successful API call"""
        self.provider_status[provider]['healthy'] = True
        self.provider_status[provider]['last_success'] = datetime.now()
        self.provider_status[provider]['consecutive_failures'] = 0
        self.provider_status[provider]['total_requests'] += 1
        
        self.logger.info(f"✅ {provider.title()} API call successful")
    
    def _record_failure(self, provider: str, error: str):
        """Record failed API call and update circuit breaker"""
        self.provider_status[provider]['consecutive_failures'] += 1
        self.provider_status[provider]['total_requests'] += 1
        
        # Check if we should open circuit breaker
        if self.provider_status[provider]['consecutive_failures'] >= self.circuit_breaker['failure_threshold']:
            self.provider_status[provider]['healthy'] = False
            self.logger.warning(f"🔴 {provider.title()} API marked unhealthy after {self.provider_status[provider]['consecutive_failures']} failures")
        
        self.logger.error(f"❌ {provider.title()} API call failed: {error}")
    
    def _is_provider_available(self, provider: str) -> bool:
        """Check if provider is available (circuit breaker logic)"""
        status = self.provider_status[provider]
        
        if status['healthy']:
            return True
        
        # Check if enough time has passed for recovery attempt
        if status['last_success']:
            time_since_last_success = datetime.now() - status['last_success']
            if time_since_last_success.total_seconds() > self.circuit_breaker['recovery_timeout']:
                self.logger.info(f"🔄 Attempting recovery for {provider.title()} API")
                return True
        
        return False
    
    def _get_best_provider(self, preferred_provider: Optional[str] = None) -> str:
        """Determine the best provider to use based on health status"""
        # If preferred provider is specified and available, use it
        if preferred_provider and self._is_provider_available(preferred_provider):
            return preferred_provider
        
        # Find the healthiest provider
        available_providers = [p for p in self.provider_status.keys() if self._is_provider_available(p)]
        
        if not available_providers:
            # All providers are down, try the one with the oldest failure
            providers_by_last_success = sorted(
                self.provider_status.items(),
                key=lambda x: x[1]['last_success'] or datetime.min,
                reverse=True
            )
            return providers_by_last_success[0][0]
        
        # Sort by consecutive failures (ascending) and last success (descending)
        best_provider = min(available_providers, key=lambda p: (
            self.provider_status[p]['consecutive_failures'],
            -(self.provider_status[p]['last_success'] or datetime.min).timestamp()
        ))
        
        return best_provider
    
    def _exponential_backoff_retry(self, func, max_retries: int = 3, base_delay: float = 1.0) -> str:
        """Execute function with exponential backoff retry"""
        for attempt in range(max_retries + 1):
            try:
                return func()
            except Exception as e:
                if attempt == max_retries:
                    raise e
                
                delay = base_delay * (2 ** attempt)
                self.logger.warning(f"⚠️ Attempt {attempt + 1} failed, retrying in {delay}s: {str(e)}")
                time.sleep(delay)
        
        # This should never be reached, but just in case
        raise Exception("All retry attempts exhausted")
    
    def llm_complete(self, prompt: str, provider: Optional[str] = None, **kwargs) -> str:
        """
        Complete text using LLM with automatic failover and self-healing
        
        Args:
            prompt: The input prompt
            provider: Preferred provider ('groq' or 'google'), None for auto-selection
            **kwargs: Additional parameters for the API call
        
        Returns:
            Generated text response
        """
        # Determine which provider to use
        selected_provider = self._get_best_provider(provider)
        
        self.logger.info(f"🤖 Using {selected_provider.title()} API for completion")
        
        # Define the API call function
        def make_api_call():
            if selected_provider == 'groq':
                return self._call_groq_api(prompt, **kwargs)
            elif selected_provider == 'google':
                return self._call_google_api(prompt, **kwargs)
            else:
                raise Exception(f"Unknown provider: {selected_provider}")
        
        # Try the selected provider with retries
        try:
            return self._exponential_backoff_retry(
                make_api_call, 
                max_retries=self.circuit_breaker['max_retries']
            )
        except Exception as e:
            # If selected provider fails completely, try the other one
            fallback_providers = [p for p in ['groq', 'google'] if p != selected_provider]
            
            for fallback_provider in fallback_providers:
                if self._is_provider_available(fallback_provider):
                    self.logger.warning(f"🔄 Falling back to {fallback_provider.title()} API")
                    
                    def fallback_api_call():
                        if fallback_provider == 'groq':
                            return self._call_groq_api(prompt, **kwargs)
                        elif fallback_provider == 'google':
                            return self._call_google_api(prompt, **kwargs)
                    
                    try:
                        return self._exponential_backoff_retry(
                            fallback_api_call,
                            max_retries=self.circuit_breaker['max_retries']
                        )
                    except Exception as fallback_error:
                        self.logger.error(f"❌ Fallback to {fallback_provider.title()} also failed: {str(fallback_error)}")
                        continue
            
            # All providers failed
            error_msg = f"❌ All LLM providers failed. Last error: {str(e)}"
            self.logger.error(error_msg)
            return f"Error: {error_msg}"
    
    def health_check(self) -> Dict[str, Any]:
        """Perform health check on all providers"""
        self.logger.info("🩺 Performing LLM providers health check")
        
        health_status = {
            'timestamp': datetime.now().isoformat(),
            'providers': {},
            'overall_health': 'healthy'
        }
        
        test_prompt = "Say 'test'"
        
        for provider in ['groq', 'google']:
            try:
                start_time = time.time()
                
                if provider == 'groq':
                    result = self._call_groq_api(test_prompt, max_tokens=10)
                else:
                    result = self._call_google_api(test_prompt, max_tokens=10)
                
                response_time = time.time() - start_time
                
                health_status['providers'][provider] = {
                    'healthy': True,
                    'response_time': response_time,
                    'status': self.provider_status[provider].copy(),
                    'last_result': result[:50] + '...' if len(result) > 50 else result
                }
                
            except Exception as e:
                health_status['providers'][provider] = {
                    'healthy': False,
                    'error': str(e),
                    'status': self.provider_status[provider].copy()
                }
                health_status['overall_health'] = 'degraded'
        
        # Check if any provider is healthy
        healthy_providers = [p for p, status in health_status['providers'].items() if status['healthy']]
        if not healthy_providers:
            health_status['overall_health'] = 'critical'
        
        self.last_health_check = datetime.now()
        return health_status
    
    def reset_circuit_breakers(self):
        """Reset all circuit breakers (force recovery attempt)"""
        self.logger.info("🔄 Resetting all circuit breakers")
        for provider in self.provider_status:
            self.provider_status[provider]['healthy'] = True
            self.provider_status[provider]['consecutive_failures'] = 0
    
    def get_status(self) -> Dict[str, Any]:
        """Get current router status"""
        return {
            'provider_status': self.provider_status.copy(),
            'circuit_breaker_config': self.circuit_breaker.copy(),
            'last_health_check': self.last_health_check.isoformat() if self.last_health_check else None,
            'available_providers': [p for p in self.provider_status.keys() if self._is_provider_available(p)]
        }

# Global instance for easy access
enhanced_llm_router = EnhancedLLMRouter()

def llm_complete_with_healing(prompt: str, provider: Optional[str] = None, **kwargs) -> str:
    """
    Wrapper function for compatibility with existing code
    """
    return enhanced_llm_router.llm_complete(prompt, provider, **kwargs)