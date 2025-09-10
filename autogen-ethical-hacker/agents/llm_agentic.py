"""
This module integrates Microsoft AutoGen's agentic AI with your pentest tool suite.
It enables LLM-driven orchestration, multi-agent collaboration, and advanced planning.
"""

from autogen_agentchat.agents import AssistantAgent
from llm.llm_complete_wrapper import LLMCompleteWrapper


# Example: Wrap a pentest tool as a function
def nmap_scan_tool(target: str) -> str:
    import subprocess
    result = subprocess.run(["nmap", "-A", target], capture_output=True, text=True)
    return result.stdout

# Create an LLM agent with tool access
def create_llm_pentest_agent():
    agent = AssistantAgent(
        "pentest_llm_agent",
        system_message="You are an advanced pentest agent. Use tools to gather information and exploit targets.",
        tools=[nmap_scan_tool],
        model_client=LLMCompleteWrapper(),
    )
    return agent
