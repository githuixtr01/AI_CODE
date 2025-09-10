import json
import os
import sys
from agents.orchestrator_agent import OrchestratorAgent

def load_json(filename):
    path = os.path.join(os.path.dirname(__file__), "config", filename)
    with open(path, "r") as f:
        return json.load(f)

# Add the project root to the Python path to allow imports from other folders
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Add autogen-agentchat src to sys.path for import resolution
agentchat_src = os.path.abspath(os.path.join(os.path.dirname(__file__), '../autogen-official/python/packages/autogen-agentchat/src'))
if agentchat_src not in sys.path:
    sys.path.insert(0, agentchat_src)

apis = load_json("apis.json")
lab_scope = load_json("lab_scope.json")
tools_config = load_json("tools_config.json")

def display_banner():
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                    🚀 AutoGen Ethical Hacker                  ║
    ║                      Ultra-Agentic Beast                      ║
    ║              AI-Powered Penetration Testing Suite             ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)

def display_menu():
    print("""
    🎯 PENETRATION TESTING OPERATIONS:
    
    1.  🔍 Full Network Reconnaissance & Mapping
    2.  🌐 Advanced Web Application Testing
    3.  🔒 Vulnerability Assessment & Analysis  
    4.  💥 Automated Exploitation & Post-Exploitation
    5.  🕵️  Social Engineering & OSINT Analysis
    6.  🔐 Cryptographic Analysis & Certificate Testing
    7.  📱 IoT & Embedded Device Exploitation
    8.  🔄 Lateral Movement & Privilege Escalation
    9.  📊 Network Traffic Analysis & Monitoring
    10. 🎭 Steganography & Covert Communications
    11. 🧬 AI-Powered Custom Payload Generation
    12. 💾 Data Exfiltration & Sensitive Data Mining
    13. 🛡️  Blue Team Evasion & Anti-Forensics
    14. 📋 Comprehensive Security Report Generation
    15. 🎲 Custom Task (Describe your objective)
    
    0.  🚪 Exit
    """)

def get_user_choice():
    while True:
        try:
            choice = input("\n🎯 Select your mission (0-15): ").strip()
            if choice.isdigit() and 0 <= int(choice) <= 15:
                return int(choice)
            else:
                print("❌ Invalid choice. Please enter a number between 0-15.")
        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            return 0

def get_custom_task():
    print("\n🎯 CUSTOM TASK CONFIGURATION:")
    task = input("📝 Describe your objective: ").strip()
    target = input("🎯 Target(s) (IP/domain/range): ").strip()
    scope = input("🔍 Scope limitations: ").strip()
    return {
        "task": task,
        "target": target, 
        "scope": scope
    }

def main():
    display_banner()
    
    orchestrator = OrchestratorAgent(apis, lab_scope, tools_config)
    
    while True:
        display_menu()
        choice = get_user_choice()
        
        if choice == 0:
            print("👋 Thanks for using AutoGen Ethical Hacker!")
            break
        elif choice == 1:
            print("🔍 Starting Full Network Reconnaissance...")
            orchestrator.run_task("Full network reconnaissance and mapping")
        elif choice == 2:
            print("🌐 Initiating Advanced Web Application Testing...")
            orchestrator.run_task("Advanced web application penetration testing")
        elif choice == 3:
            print("🔒 Beginning Vulnerability Assessment...")
            orchestrator.run_task("Comprehensive vulnerability assessment and analysis")
        elif choice == 4:
            print("💥 Starting Automated Exploitation...")
            orchestrator.run_task("Automated exploitation and post-exploitation")
        elif choice == 5:
            print("🕵️ Launching Social Engineering Analysis...")
            orchestrator.run_task("Social engineering and OSINT analysis")
        elif choice == 6:
            print("🔐 Starting Cryptographic Analysis...")
            orchestrator.run_task("Cryptographic analysis and certificate testing")
        elif choice == 7:
            print("📱 Initiating IoT Device Exploitation...")
            orchestrator.run_task("IoT and embedded device exploitation")
        elif choice == 8:
            print("🔄 Starting Lateral Movement Analysis...")
            orchestrator.run_task("Lateral movement and privilege escalation")
        elif choice == 9:
            print("📊 Beginning Network Traffic Analysis...")
            orchestrator.run_task("Network traffic analysis and monitoring")
        elif choice == 10:
            print("🎭 Starting Steganography Analysis...")
            orchestrator.run_task("Steganography and covert communications analysis")
        elif choice == 11:
            print("🧬 Generating AI-Powered Custom Payloads...")
            orchestrator.run_task("AI-powered custom payload generation")
        elif choice == 12:
            print("💾 Starting Data Exfiltration Analysis...")
            orchestrator.run_task("Data exfiltration and sensitive data mining")
        elif choice == 13:
            print("🛡️ Initiating Blue Team Evasion...")
            orchestrator.run_task("Blue team evasion and anti-forensics")
        elif choice == 14:
            print("📋 Generating Comprehensive Security Report...")
            orchestrator.run_task("Generate comprehensive security assessment report")
        elif choice == 15:
            custom = get_custom_task()
            print(f"🎲 Starting Custom Task: {custom['task']}")
            orchestrator.run_custom_task(custom)
        
        input("\n⏳ Press Enter to continue...")

if __name__ == "__main__":
    main()
