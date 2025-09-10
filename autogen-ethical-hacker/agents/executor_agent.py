from autogen_agentchat.agents import AssistantAgent
from sandbox.docker_runner import run_in_sandbox
from groq import Groq


class ExecutorAgent(AssistantAgent):
    def __init__(self, apis, lab_scope, tools_config):
        groq_api = apis.get('groq', {}).get('api_key', '')
        self.groq_client = Groq(api_key=groq_api)
        super().__init__(
            name="ExecutorAgent",
            model_client=self.groq_client,
            system_message="You execute tasks in Docker sandbox for safety and isolation."
        )
        self.lab_scope = lab_scope
        self.tools_config = tools_config
        self.local_tools = {}
        self.local_tools['run_in_sandbox_tool'] = self.run_in_sandbox_tool

    def run_in_sandbox_tool(self, analysis_results):
        if not analysis_results:
            print("[ExecutorAgent] No analysis results provided.")
            return False
        try:
            return run_in_sandbox(analysis_results)
        except Exception as e:
            print(f"[ExecutorAgent] Sandbox execution failed: {e}")
            return False

    def run(self, analysis_results):
        results = self.run_in_sandbox_tool(analysis_results)
        print(f"[ExecutorAgent] Executed tasks in sandbox.")
        return results
