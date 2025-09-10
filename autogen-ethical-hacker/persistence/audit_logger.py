def generate_report(pentest_context):
    # Now generates a comprehensive report from the full context
    print(f"[AuditLogger] Generating comprehensive report...")
    with open('report.json', 'w') as f:
        import json
        json.dump(pentest_context, f, indent=2)
    print("[AuditLogger] Report saved as report.json")
    return "report.json"
