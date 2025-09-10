"""
Blue Team / Adversarial Simulation
Uses OpenAI LLM to analyze findings and suggest defensive actions.
"""

from llm.llm_router import llm_complete

def run_blue_team_simulation(findings):
    """Simulate blue team response using LLM."""
    print(f"[blue_team] Simulating blue team for findings: {findings}")
    findings_text = "\n".join([str(f) for f in findings])
    prompt = f"You are a blue team security analyst. Given these pentest findings, suggest detection, response, and remediation actions.\nFindings:\n{findings_text}"
    try:
        blue_team_response = llm_complete(prompt, provider="groq")
        print(f"[blue_team] LLM response: {blue_team_response}")
        return {"status": "ok", "findings": findings, "blue_team_response": blue_team_response}
    except Exception as e:
        print(f"[blue_team] Error: {e}")
        return {"status": "error", "findings": findings, "error": str(e)}
