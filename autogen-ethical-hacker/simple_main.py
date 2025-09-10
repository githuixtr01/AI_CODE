#!/usr/bin/env python3
"""
Simple AutoGen Ethical Hacker - Working Version
Core functionality without complex dependencies
"""

import os
import sys
import json
import time
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

# Import working components
from tools.nmap_tool import run_nmap
from tools.sqlmap_tool import run_sqlmap
from tools.nikto_tool import run_nikto
from tools.masscan_tool import run_masscan
from llm.simple_llm_router import llm_complete

# Optional imports (may fail due to dependencies)
try:
    from system.api_quota_manager import APIQuotaManager
except ImportError:
    APIQuotaManager = None
    
try:
    from system.stealth_manager import StealthManager
except ImportError:
    StealthManager = None

class SimpleEthicalHacker:
    def __init__(self):
        self.banner = """
╔══════════════════════════════════════════════════════════════════╗
║                    🚀 AutoGen Ethical Hacker                     ║
║                      Simple Working Version                      ║
║                AI-Powered Penetration Testing Suite              ║
╚══════════════════════════════════════════════════════════════════╝
        """
        
        # Load configurations
        try:
            with open('config/lab_scope.json', 'r') as f:
                self.lab_scope = json.load(f)
        except:
            self.lab_scope = {"allowed_targets": ["127.0.0.1", "192.168.1.0/24"]}
        
        try:
            with open('config/tools_config.json', 'r') as f:
                self.tools_config = json.load(f)
        except:
            self.tools_config = {"nmap_path": "nmap", "sqlmap_path": "sqlmap"}
        
        # Initialize managers (optional)
        self.api_manager = None
        self.stealth_manager = None
        
        try:
            if APIQuotaManager:
                self.api_manager = APIQuotaManager()
        except Exception as e:
            print(f"Warning: API manager failed: {e}")
            
        try:
            if StealthManager:
                self.stealth_manager = StealthManager()
        except Exception as e:
            print(f"Warning: Stealth manager failed: {e}")
    
    def display_banner(self):
        print(self.banner)
    
    def display_menu(self):
        print("""
🎯 PENETRATION TESTING OPERATIONS:

1.  🔍 Network Reconnaissance (Nmap)
2.  🌐 Web Vulnerability Testing (SQLMap)
3.  🔒 Web Server Analysis (Nikto)
4.  ⚡ Fast Port Scanning (Masscan)
5.  🤖 AI Analysis of Results
6.  📊 System Status
7.  👻 Ghost Mode Operations
8.  🎲 Custom Task
0.  🚪 Exit
        """)
    
    def run_reconnaissance(self, target=None):
        if not target:
            target = input("Enter target IP/hostname: ").strip()
        
        if not self.validate_target(target):
            print("❌ Target not in allowed scope!")
            return None
        
        print(f"🔍 Running Nmap scan on {target}...")
        results = run_nmap([target])
        print("✅ Nmap scan completed")
        return results
    
    def run_web_testing(self, target=None):
        if not target:
            target = input("Enter target URL: ").strip()
        
        print(f"🌐 Running SQLMap on {target}...")
        results = run_sqlmap(target, ["--batch", "--level=1", "--risk=1"])
        print("✅ SQLMap scan completed")
        return results
    
    def run_web_analysis(self, target=None):
        if not target:
            target = input("Enter target URL: ").strip()
        
        print(f"🔒 Running Nikto on {target}...")
        results = run_nikto(target, ["-C", "all"])
        print("✅ Nikto scan completed")
        return results
    
    def run_port_scan(self, target=None):
        if not target:
            target = input("Enter target IP: ").strip()
        
        if not self.validate_target(target):
            print("❌ Target not in allowed scope!")
            return None
        
        print(f"⚡ Running Masscan on {target}...")
        results = run_masscan([target], "1-1000")
        print("✅ Masscan completed")
        return results
    
    def ai_analysis(self):
        print("🤖 AI Analysis Mode")
        findings = input("Enter your findings or scan results: ").strip()
        
        prompt = f"""
        As a cybersecurity expert, analyze the following penetration testing findings:
        
        {findings}
        
        Please provide:
        1. Summary of vulnerabilities found
        2. Risk assessment (Critical/High/Medium/Low)
        3. Recommended remediation steps
        4. Next testing steps
        """
        
        print("🤖 Analyzing with AI...")
        # Try Groq first, fallback to Google
        result = llm_complete(prompt, provider="groq")
        if "Error:" in result:
            print("Groq failed, trying Google...")
            result = llm_complete(prompt, provider="google")
        
        print("🤖 AI Analysis Results:")
        print("-" * 60)
        print(result)
        print("-" * 60)
        
        return result
    
    def system_status(self):
        print("\n📊 SYSTEM STATUS")
        print("=" * 60)
        
        # Check API keys
        groq_key = "✅" if os.environ.get("GROQ_API_KEY") else "❌"
        google_key = "✅" if os.environ.get("GOOGLE_API_KEY") else "❌"
        
        print(f"🔑 Groq API Key: {groq_key}")
        print(f"🔑 Google API Key: {google_key}")
        
        # Test tools
        tools_status = {
            "nmap": self.test_tool("nmap --version"),
            "sqlmap": self.test_tool("sqlmap --version"),
            "nikto": self.test_tool("nikto -Version"),
            "masscan": self.test_tool("masscan --version")
        }
        
        print("\n🛠️ Security Tools:")
        for tool, status in tools_status.items():
            emoji = "✅" if status else "❌"
            print(f"  {emoji} {tool}")
        
        # System info
        import platform
        print(f"\n🖥️  System: {platform.system()} {platform.release()}")
        print(f"🐍 Python: {platform.python_version()}")
        
        return True
    
    def test_tool(self, command):
        try:
            import subprocess
            result = subprocess.run(command.split(), capture_output=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def validate_target(self, target):
        # Simple validation - check if target is in allowed scope
        allowed = self.lab_scope.get("allowed_targets", [])
        return any(target.startswith(allowed_target.split('/')[0]) for allowed_target in allowed)
    
    def ghost_mode(self):
        print("👻 GHOST MODE OPERATIONS")
        print("=" * 60)
        
        if self.stealth_manager:
            try:
                status = self.stealth_manager.stealth_status()
                print(f"🌐 External IP: {status['external_ip']}")
                print(f"👻 Ghost Mode: {status.get('stealth_level', 'Normal')}")
                print("🔒 Anonymization features available but require root privileges")
            except Exception as e:
                print(f"Stealth manager error: {e}")
        else:
            print("👻 Ghost Mode: Basic stealth features available")
            print("🔒 Advanced features require proper dependencies")
        
        return True
    
    def custom_task(self):
        print("🎲 CUSTOM TASK MODE")
        task_description = input("Describe your penetration testing objective: ").strip()
        
        prompt = f"""
        You are a penetration testing expert. Create a step-by-step plan for this objective:
        
        {task_description}
        
        Provide a detailed methodology with:
        1. Reconnaissance steps
        2. Vulnerability identification
        3. Exploitation techniques
        4. Post-exploitation activities
        5. Reporting requirements
        """
        
        print("🤖 Creating custom penetration testing plan...")
        plan = llm_complete(prompt, provider="groq")
        
        if "Error:" in plan:
            plan = llm_complete(prompt, provider="google")
        
        print("🎲 Custom Task Plan:")
        print("-" * 60)
        print(plan)
        print("-" * 60)
        
        execute = input("Execute this plan? (y/n): ").strip().lower()
        if execute == 'y':
            print("⚠️  Custom execution would require additional implementation")
            print("This is a planning tool - manual execution required")
        
        return plan
    
    def run(self):
        """Main application loop"""
        self.display_banner()
        
        while True:
            self.display_menu()
            choice = input("\n🎯 Select operation (0-8): ").strip()
            
            print()  # Add spacing
            
            if choice == "1":
                self.run_reconnaissance()
            elif choice == "2":
                self.run_web_testing()
            elif choice == "3":
                self.run_web_analysis()
            elif choice == "4":
                self.run_port_scan()
            elif choice == "5":
                self.ai_analysis()
            elif choice == "6":
                self.system_status()
            elif choice == "7":
                self.ghost_mode()
            elif choice == "8":
                self.custom_task()
            elif choice == "0":
                print("👋 Goodbye! Stay ethical!")
                break
            else:
                print("❌ Invalid choice. Please try again.")
            
            input("\nPress Enter to continue...")
            print("\n" + "="*80 + "\n")

def main():
    try:
        hacker = SimpleEthicalHacker()
        hacker.run()
    except KeyboardInterrupt:
        print("\n\n🛑 Operation interrupted by user")
    except Exception as e:
        print(f"\n❌ Critical error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()