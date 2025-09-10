"""
Explainability Agent
Uses OpenAI LLM to summarize/explain a step and its context.
"""

from llm.llm_router import llm_complete

def explain_step(step, context=None):
    """Summarize/explain a step and its context using LLM."""
    print(f"[explainability] Explaining step: {step}")
    prompt = f"Explain the following pentest step in plain language.\nStep: {step}"
    if context:
        prompt += f"\nContext: {context}"
    try:
        explanation = llm_complete(prompt, provider="groq")
        print(f"[explainability] LLM explanation: {explanation}")
        return explanation
    except Exception as e:
        print(f"[explainability] Error: {e}")
        return f"Explanation for: {step} (error: {e})"
