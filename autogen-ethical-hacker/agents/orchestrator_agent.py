from agents.agent_factory import AgentFactory
import json

class OrchestratorAgent:
    def __init__(self, apis, lab_scope, tools_config):
        """
        The Orchestrator is the master planner. It receives high-level goals,
        manages the overall state of the operation, and uses the AgentFactory
        to execute workflows and spawn sub-teams.
        """
        self.agent_factory = AgentFactory(apis, lab_scope, tools_config)
        self.pentest_context = {
            "task": None,
            "recon": {"status": "pending", "results": {}},
            "vuln": {"status": "pending", "results": {}},
            "exploit": {"status": "pending", "results": {}},
            "analysis": {"status": "pending", "results": {}},
            "execution": {"status": "pending", "results": {}},
            "report": {"status": "pending", "results": {}},
            "history": []
        }

    def run_task(self, task):
        print(f"[Orchestrator] Starting task: {task}")
        self.pentest_context['task'] = task
        self.agent_factory.execute_task_flow(self.pentest_context)
        print(f"[Orchestrator] Task finished. Final state:\n{json.dumps(self.pentest_context, indent=2)}")
    
    def run_custom_task(self, custom_config):
        print(f"[Orchestrator] Starting custom task: {custom_config['task']}")
        self.pentest_context['task'] = custom_config['task']
        self.pentest_context['custom_target'] = custom_config['target']
        self.pentest_context['custom_scope'] = custom_config['scope']
        self.agent_factory.execute_custom_task_flow(self.pentest_context, custom_config)
        print(f"[Orchestrator] Custom task finished.")

    def run(self, task):
        """
        Entry point for running a standard task. Delegates to run_task.
        """
        self.run_task(task)
