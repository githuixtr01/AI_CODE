# AutoGen imports

from autogen_agentchat.agents import AssistantAgent
from tools.nmap_tool import run_nmap
from groq import Groq


class ReconAgent(AssistantAgent):
    def __init__(self, apis, lab_scope, tools_config):
        groq_api = apis.get('groq', {}).get('api_key', '')
        google_api = apis.get('google', {}).get('api_key', '')

        # Initialize Groq client
        self.groq_client = Groq(api_key=groq_api)
        super().__init__(
            name="ReconAgent",
            model_client=self.groq_client,  # Pass Groq client as model_client
            system_message="You are a reconnaissance specialist. Your goal is to perform network scans and enumeration on the targets defined in the scope. You must use the 'run_nmap_scan' tool to gather information about open ports, services, and versions. Once you have the results, clearly state that reconnaissance is complete and pass the findings on for vulnerability analysis."
        )
        self.lab_scope = lab_scope
        self.tools_config = tools_config
        self.results = None
        self.local_tools = {}
        self.local_tools['run_nmap_scan'] = self.run_nmap_scan

    def run_nmap_scan(self, targets):
        print("[ReconAgent] (Nmap disabled for this run)")
        return {"nmap": "disabled"}

    def run(self, task):
        import socket
        print(f"[ReconAgent] Received task: {task}")
        # Try to extract a real target from the task string, fallback to allowed_targets
        targets = []
        if isinstance(task, str):
            task = task.strip()
            print(f"[ReconAgent] Attempting to resolve target from task: {task}")
            if any(char.isdigit() for char in task) or "." in task:
                try:
                    ip = socket.gethostbyname(task.split()[0])
                    print(f"[ReconAgent] Resolved {task.split()[0]} to {ip}")
                    targets = [ip]
                except Exception as e:
                    print(f"[ReconAgent] Could not resolve {task.split()[0]}: {e}")
        if not targets:
            # Prefer CLI --target if available in task, else fallback to lab_scope
            cli_target = None
            if hasattr(self, 'cli_target') and self.cli_target:
                cli_target = self.cli_target
            if cli_target:
                targets = [cli_target]
                print(f"[ReconAgent] Using CLI target: {cli_target}")
            else:
                targets = self.lab_scope.get('allowed_targets', [])
                print(f"[ReconAgent] Using allowed_targets from lab_scope: {targets}")
        self.results = self.run_nmap_scan(targets)
        print(f"[ReconAgent] Scan results: {self.results}")
        return self.results

    def get_results(self):
        return self.results
