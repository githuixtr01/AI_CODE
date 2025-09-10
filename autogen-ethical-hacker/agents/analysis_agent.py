# AutoGen imports

from autogen_agentchat.agents import AssistantAgent
from llm.multi_api_manager import llm_ensemble_reasoning
from groq import Groq


class AnalysisAgent(AssistantAgent):
    def __init__(self, apis, lab_scope, tools_config):
        groq_api = apis.get('groq', {}).get('api_key', '')
        google_api = apis.get('google', {}).get('api_key', '')
        self.groq_client = Groq(api_key=groq_api)
        super().__init__(
            name="AnalysisAgent",
            model_client=self.groq_client,
            system_message="You perform ensemble reasoning and risk analysis using Groq and Gemini."
        )
        self.lab_scope = lab_scope
        self.tools_config = tools_config
        self.results = None
        self.local_tools = {}
        self.local_tools['ensemble_reasoning_tool'] = self.ensemble_reasoning_tool

    def ensemble_reasoning_tool(self, exploit_results):
        if not exploit_results:
            print("[AnalysisAgent] No exploit results provided.")
            return {}
        try:
            # Use Groq client for completion
            completion = self.groq_client.chat.completions.create(
                model="groq/llama3-70b-8192",
                messages=[
                    {
                        "role": "user",
                        "content": str(exploit_results)
                    }
                ],
                temperature=1,
                max_completion_tokens=8192,
                top_p=1,
                reasoning_effort="medium",
                stream=True,
                stop=None
            )
            response = ""
            for chunk in completion:
                response += chunk.choices[0].delta.content or ""
            return {"groq_analysis": response}
        except Exception as e:
            print(f"[AnalysisAgent] Groq analysis failed: {e}")
            return {"error": str(e)}

    def run(self, exploit_results):
        self.results = self.ensemble_reasoning_tool(exploit_results)
        print(f"[AnalysisAgent] Analysis results: {self.results}")
        return self.results
