# AutoGen imports

from autogen_agentchat.agents import AssistantAgent
from persistence.audit_logger import generate_report
from groq import Groq


class ReportAgent(AssistantAgent):
    def __init__(self, apis, lab_scope, tools_config):
        groq_api = apis.get('groq', {}).get('api_key', '')
        self.groq_client = Groq(api_key=groq_api)
        super().__init__(
            name="ReportAgent",
            model_client=self.groq_client,
            system_message="You generate structured reports and audit logs for all findings."
        )
        self.lab_scope = lab_scope
        self.tools_config = tools_config
        self.local_tools = {}
        self.local_tools["generate_report_tool"] = self.generate_report_tool

    def generate_report_tool(self, pentest_context):
        if not pentest_context:
            print("[ReportAgent] No pentest context provided.")
            return None
        try:
            return generate_report(pentest_context)
        except Exception as e:
            print(f"[ReportAgent] Report generation failed: {e}")
            return None

    def run(self, pentest_context):
        report = self.generate_report_tool(pentest_context)
        print(f"[ReportAgent] Report generated.")
        return report
