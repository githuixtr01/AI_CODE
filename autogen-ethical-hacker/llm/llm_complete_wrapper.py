import asyncio
class LLMCompleteWrapper:
    """Wraps llm_complete function to provide model_info property and async callable interface, with Gemini 1.5 Pro fallback."""
    def __init__(self, provider="groq", model=None):
        self.provider = provider
        self.model = model or ("openai/gpt-oss-120b" if provider == "groq" else "gemini-1.5-pro")
        self._model_info = {
            "provider": self.provider,
            "model": self.model,
            "function_calling": True,
            "vision": False
        }
    def _ensure_str_prompt(self, prompt):
        # If prompt is a list of dicts (messages), join their content
        if isinstance(prompt, list):
            if all(isinstance(m, dict) and 'content' in m for m in prompt):
                return '\n'.join(str(m['content']) for m in prompt)
            return str(prompt)
        if isinstance(prompt, dict) and 'content' in prompt:
            return str(prompt['content'])
        return str(prompt)
    async def __call__(self, prompt, **kwargs):
        # Remove unsupported args
        unsupported = [
            'cancellation_token', 'json_output', 'extra_create_args', 'tools', 'tool_choice'
        ]
        for key in unsupported:
            kwargs.pop(key, None)
        prompt = self._ensure_str_prompt(prompt)
        from llm.llm_router import llm_complete
        loop = asyncio.get_event_loop()
        try:
            result = await loop.run_in_executor(None, llm_complete, prompt, self.provider, self.model, **kwargs)
            if result:
                return result
        except Exception:
            pass
        # Fallback to Gemini 1.5 Pro if Groq fails
        try:
            result = await loop.run_in_executor(None, llm_complete, prompt, "gemini", "gemini-1.5-pro", **kwargs)
            return result
        except Exception as e:
            return f"[LLM Error] Both Groq and Gemini 1.5 Pro failed: {e}"
    async def create(self, *args, **kwargs):
        # Remove unsupported args
        unsupported = [
            'cancellation_token', 'json_output', 'extra_create_args', 'tools', 'tool_choice'
        ]
        for key in unsupported:
            kwargs.pop(key, None)
        if args:
            args = (self._ensure_str_prompt(args[0]),) + args[1:]
        return await self.__call__(*args, **kwargs)
    @property
    def model_info(self):
        return self._model_info
