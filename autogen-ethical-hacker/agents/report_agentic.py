"""
Automated report generation using LLMs for pentest findings.
"""
from autogen_agentchat.agents import AssistantAgent
from llm.llm_complete_wrapper import LLMCompleteWrapper

def generate_pentest_report(findings: list, target: str) -> str:
    """
    findings: list of dicts, each with keys: 'title', 'description', 'evidence', 'remediation'
    target: scanned target
    """
    agent = AssistantAgent(
        "report_agent",
        system_message="You are a cybersecurity expert. Write a detailed, professional pentest report based on the findings provided.",
        model_client=LLMCompleteWrapper(),
    )
    findings_text = "\n".join([
        f"Title: {f['title']}\nDescription: {f['description']}\nEvidence: {f['evidence']}\nRemediation: {f['remediation']}\n" for f in findings
    ])
    prompt = f"Generate a pentest report for target {target} with the following findings.\n\n{findings_text}"
    import asyncio
    result = asyncio.run(agent.run(task=prompt))
    # Try to extract text from common TaskResult fields
    for attr in ("content", "text", "result", "output"):
        if hasattr(result, attr):
            val = getattr(result, attr)
            if isinstance(val, str):
                return val
    return str(result)
