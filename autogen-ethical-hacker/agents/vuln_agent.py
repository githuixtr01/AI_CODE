# AutoGen imports

from autogen_agentchat.agents import AssistantAgent
from tools.cve_lookup import lookup_cves
from groq import Groq


class VulnAgent(AssistantAgent):
    def __init__(self, apis, lab_scope, tools_config):
        groq_api = apis.get('groq', {}).get('api_key', '')
        self.groq_client = Groq(api_key=groq_api)
        super().__init__(
            name="VulnAgent",
            model_client=self.groq_client,
            system_message="You map services to CVEs and assess vulnerabilities."
        )
        self.lab_scope = lab_scope
        self.tools_config = tools_config
        self.results = None
        self.local_tools = {}
        self.local_tools['lookup_cves_tool'] = self.lookup_cves_tool

    def lookup_cves_tool(self, recon_results):
        if not recon_results:
            print("[VulnAgent] No recon results provided.")
            return {}
        try:
            return lookup_cves(recon_results)
        except Exception as e:
            print(f"[VulnAgent] CVE lookup failed: {e}")
            return {"error": str(e)}

    def run(self, recon_results):
        self.results = self.lookup_cves_tool(recon_results)
        print(f"[VulnAgent] Vulnerability results: {self.results}")
        return self.results
