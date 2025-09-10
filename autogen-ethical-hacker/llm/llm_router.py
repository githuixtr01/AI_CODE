"""
LLM Router: Unified interface for Groq and Gemini LLMs.
Chooses provider based on argument or fallback order.
"""
import os
from groq import Groq
import google.generativeai as genai

def llm_complete(prompt, provider="groq", model=None, **kwargs):
    """Unified LLM completion for Groq (streaming, openai/gpt-oss-120b) and Gemini."""
    if provider == "groq":
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY not set")
        client = Groq(api_key=api_key)
        model = model or "openai/gpt-oss-120b"
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=kwargs.get("temperature", 1),
            max_completion_tokens=kwargs.get("max_completion_tokens", 8192),
            top_p=kwargs.get("top_p", 1),
            reasoning_effort=kwargs.get("reasoning_effort", "medium"),
            stream=True,
            stop=kwargs.get("stop", None)
        )
        result = ""
        for chunk in completion:
            result += chunk.choices[0].delta.content or ""
        return result
    elif provider == "gemini":
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY not set")
        client = genai.Client()
        model = model or "gemini-1.5-pro"
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )
        return response.text
    else:
        raise ValueError(f"Unknown provider: {provider}")
