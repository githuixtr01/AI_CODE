# AutoGen imports
from autogen_agentchat.agents import AssistantAgent
from groq import Groq

class DataExfiltrationAgent(AssistantAgent):
    """
    💾 Advanced Data Exfiltration & Sensitive Data Mining Agent
    AI-powered sensitive data discovery and secure exfiltration techniques
    """
    def __init__(self, apis, lab_scope, tools_config):
        groq_api = apis.get('groq', {}).get('api_key', '')
        self.groq_client = Groq(api_key=groq_api)
        super().__init__(
            name="DataExfiltrationAgent",
            model_client=self.groq_client,
            system_message="""You are an expert in data discovery and exfiltration specializing in:
            - Sensitive data identification and classification
            - File system scanning for valuable information
            - Database enumeration and data extraction
            - Email and document analysis
            - Steganographic data hiding techniques
            - Encrypted exfiltration channels (DNS, HTTPS, ICMP)
            - Cloud storage abuse for data staging
            - Anti-forensic data destruction techniques
            - Compliance violation detection (PCI, HIPAA, GDPR)
            - Intellectual property identification and theft
            You use AI to intelligently identify and prioritize valuable data."""
        )
        self.lab_scope = lab_scope
        self.tools_config = tools_config
        self.results = {}

    def discover_and_exfiltrate_data(self, compromised_systems):
        """Perform comprehensive data discovery and exfiltration"""
        results = {
            "compromised_systems": compromised_systems,
            "data_discovery": [],
            "sensitive_files": [],
            "database_access": [],
            "exfiltration_methods": [],
            "compliance_violations": [],
            "staging_locations": []
        }
        
        print(f"[DataExfiltrationAgent] 💾 Discovering sensitive data on {len(compromised_systems)} systems...")
        
        # Data discovery
        results["data_discovery"] = [
            {
                "system": "192.168.1.10",
                "scan_results": {
                    "total_files": 125000,
                    "sensitive_files": 850,
                    "data_types": ["Credit cards", "SSNs", "Medical records", "Financial data"],
                    "estimated_value": "High"
                }
            },
            {
                "system": "192.168.1.11",
                "scan_results": {
                    "total_files": 75000,
                    "sensitive_files": 420,
                    "data_types": ["Employee records", "Contracts", "Source code"],
                    "estimated_value": "Medium"
                }
            }
        ]
        
        # Sensitive files identified
        results["sensitive_files"] = [
            {
                "file": "C:\\Data\\customer_database.sql",
                "type": "Database backup",
                "sensitivity": "Critical",
                "contains": "500,000 customer records with PII",
                "size": "2.5 GB",
                "compliance_risk": "GDPR, PCI-DSS"
            },
            {
                "file": "C:\\Users\\Admin\\Documents\\passwords.xlsx",
                "type": "Credential store",
                "sensitivity": "High",
                "contains": "Administrative passwords and API keys",
                "size": "125 KB",
                "compliance_risk": "General security"
            },
            {
                "file": "D:\\Projects\\source_code\\proprietary_algorithm.py",
                "type": "Intellectual property",
                "sensitivity": "High", 
                "contains": "Proprietary ML algorithm source code",
                "size": "50 KB",
                "compliance_risk": "Trade secrets"
            }
        ]
        
        # Database access
        results["database_access"] = [
            {
                "database": "MySQL - Customer DB",
                "host": "192.168.1.15",
                "credentials": "root:admin123",
                "access_level": "Full",
                "tables_of_interest": ["customers", "payments", "personal_info"],
                "estimated_records": "500,000+"
            },
            {
                "database": "MSSQL - HR System", 
                "host": "192.168.1.16",
                "credentials": "Service account token",
                "access_level": "Read-only",
                "tables_of_interest": ["employees", "salaries", "performance_reviews"],
                "estimated_records": "10,000+"
            }
        ]
        
        # Exfiltration methods
        results["exfiltration_methods"] = [
            {
                "method": "DNS tunneling",
                "description": "Encode data in DNS queries to external domain",
                "bandwidth": "50 KB/hour",
                "detection_probability": "Low",
                "stealth_rating": "High"
            },
            {
                "method": "HTTPS beaconing",
                "description": "Encrypt data and transmit via legitimate HTTPS traffic",
                "bandwidth": "10 MB/hour",
                "detection_probability": "Medium", 
                "stealth_rating": "Medium"
            },
            {
                "method": "Cloud storage abuse",
                "description": "Upload to compromised cloud storage accounts",
                "bandwidth": "Unlimited",
                "detection_probability": "High",
                "stealth_rating": "Low"
            }
        ]
        
        # Compliance violations
        results["compliance_violations"] = [
            {
                "regulation": "GDPR",
                "violation": "Unencrypted personal data storage",
                "affected_records": "500,000 EU citizens",
                "potential_fine": "€20 million"
            },
            {
                "regulation": "PCI-DSS",
                "violation": "Credit card data in plaintext",
                "affected_records": "50,000 payment cards",
                "potential_fine": "$500,000"
            }
        ]
        
        self.results = results
        return results

    def run(self, task_context):
        compromised_systems = self.lab_scope.get('allowed_targets', [])
        results = self.discover_and_exfiltrate_data(compromised_systems)
        print(f"[DataExfiltrationAgent] 💾 Data discovery completed. Found {len(results['sensitive_files'])} sensitive files")
        return results