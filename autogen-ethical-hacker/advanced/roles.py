"""
Role definitions for multi-agent chat.
"""

ROLES = [
    {"name": "ReconAgent", "description": "Performs reconnaissance and information gathering."},
    {"name": "ExploitAgent", "description": "Attempts exploitation based on recon findings."},
    {"name": "BlueTeamAgent", "description": "Simulates blue team defense and detection."},
    {"name": "ReportAgent", "description": "Documents findings and generates reports."},
]
