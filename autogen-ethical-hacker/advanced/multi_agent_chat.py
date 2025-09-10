"""
Multi-Agent Chat Orchestration
Implements a real multi-agent chat using AutoGen's UserProxyAgent, AssistantAgent, and CriticAgent.
"""

from autogen_agentchat.agents import AssistantAgent
from .roles import ROLES
from llm.llm_complete_wrapper import LLMCompleteWrapper
import asyncio

def run_multi_agent_chat(task, agents=None):
    print("[multi_agent_chat] Starting real multi-agent chat workflow...")
    # Define agents for each role
    recon = AssistantAgent(
        "ReconAgent",
        system_message=ROLES[0]["description"],
        model_client=LLMCompleteWrapper(),
    )
    exploit = AssistantAgent(
        "ExploitAgent",
        system_message=ROLES[1]["description"],
        model_client=LLMCompleteWrapper(),
    )
    blue = AssistantAgent(
        "BlueTeamAgent",
        system_message=ROLES[2]["description"],
        model_client=LLMCompleteWrapper(),
    )
    report = AssistantAgent(
        "ReportAgent",
        system_message=ROLES[3]["description"],
        model_client=LLMCompleteWrapper(),
    )

    # Critic and user proxy agents can be added here if supported in your AutoGen version

    # Shared chat context
    chat_history = []
    # Simulate a round-robin workflow
    print("[multi_agent_chat] Recon agent starts...")
    recon_msg = asyncio.run(recon.run(task=task))
    chat_history.append(("ReconAgent", recon_msg))
    print("[multi_agent_chat] Exploit agent responds...")
    exploit_msg = asyncio.run(exploit.run(task=f"Based on recon: {recon_msg}"))
    chat_history.append(("ExploitAgent", exploit_msg))
    print("[multi_agent_chat] Blue team agent responds...")
    blue_msg = asyncio.run(blue.run(task=f"Analyze exploit: {exploit_msg}"))
    chat_history.append(("BlueTeamAgent", blue_msg))
    print("[multi_agent_chat] Report agent responds...")
    report_msg = asyncio.run(report.run(task=f"Summarize findings: {recon_msg}, {exploit_msg}, {blue_msg}"))
    chat_history.append(("ReportAgent", report_msg))
    # Optionally, add a critic step if CriticAgent is available
    print("[multi_agent_chat] Workflow complete.")
    return chat_history
