"""
Compliance & Reporting Templates
Uses OpenAI LLM to map findings to compliance frameworks and generate a report.
"""

from llm.llm_router import llm_complete

def generate_compliance_report(findings, framework="PCI DSS"):
    """Generate a compliance report using LLM."""
    print(f"[compliance] Generating report for {framework}")
    findings_text = "\n".join([str(f) for f in findings])
    prompt = f"You are a compliance auditor. Map the following pentest findings to the {framework} framework and generate a professional report.\nFindings:\n{findings_text}"
    try:
        report = llm_complete(prompt, provider="groq")
        print(f"[compliance] LLM report: {report}")
        return report
    except Exception as e:
        print(f"[compliance] Error: {e}")
        return f"Compliance report for {framework} (error: {e})"
