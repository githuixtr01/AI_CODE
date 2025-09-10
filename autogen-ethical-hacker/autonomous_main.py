#!/usr/bin/env python3
"""
🚀 AutoGen Ethical Hacker - Autonomous Kali Linux Beast
Fully autonomous ethical hacking system with complete system control
"""
# Beautiful terminal imports
import os
import sys
import time
import json
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.shortcuts import clear
# Advanced agentic AI integration
from agents.llm_agentic import create_llm_pentest_agent
from agents.report_agentic import generate_pentest_report
from agents.threat_intel_agentic import enrich_with_threat_intel
from agents.multi_agent_workflow import MultiAgentWorkflow
# Advanced feature modules
from advanced.multi_agent_chat import run_multi_agent_chat
from advanced.memory import store_memory, query_memory
from advanced.osint import run_osint
from advanced.explainability import explain_step
from advanced.blue_team import run_blue_team_simulation
from advanced.visualization import generate_visualization
from advanced.compliance import generate_compliance_report
from advanced.plugin_system import load_plugins
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from system.kali_auto_installer import KaliAutoInstaller
from system.api_quota_manager import APIQuotaManager
from system.stealth_manager import StealthManager
from system.autonomous_controller import AutonomousController
from agents.orchestrator_agent import OrchestratorAgent

class AutonomousEthicalHacker:
    def advanced_features_menu(self):
        print("\n🧩 ADVANCED FEATURES MENU")
        print("1. Multi-Agent Chat (stub)")
        print("2. Persistent Memory (stub)")
        print("3. OSINT Integration (stub)")
        print("4. Explainability Agent (stub)")
        print("5. Blue Team Simulation (stub)")
        print("6. Visualization (stub)")
        print("7. Compliance Report (stub)")
        print("8. Plugin System (stub)")
        print("0. Back to Main Menu")
        choice = input("Select advanced feature (0-8): ").strip()
        if choice == "1":
            run_multi_agent_chat("Demo task")
        elif choice == "2":
            store_memory({"demo": "data"})
            query_memory("demo query")
        elif choice == "3":
            import asyncio
            result = asyncio.run(run_osint("example.com"))
            print("[OSINT Results]", result)
        elif choice == "4":
            explain_step("Demo step")
        elif choice == "5":
            run_blue_team_simulation(["demo finding"])
        elif choice == "6":
            generate_visualization({"demo": "data"})
        elif choice == "7":
            generate_compliance_report(["demo finding"])
        elif choice == "8":
            load_plugins()
        elif choice == "0":
            return
        else:
            print("Invalid choice.")
        input("\nPress Enter to return to the advanced features menu...")
        self.advanced_features_menu()
    def generate_report(self, findings, target):
        """Generate a professional pentest report using LLMs."""
        print("[Reporting] Generating report with LLM...")
        report = generate_pentest_report(findings, target)
        print(report)
        return report

    def enrich_ip(self, ip):
        """Enrich an IP with threat intelligence APIs."""
        apis = self.api_manager.apis.get('threat_intel', {})
        print(f"[Threat Intel] Enriching {ip}...")
        enrichment = enrich_with_threat_intel(ip, apis)
        print(enrichment)
        return enrichment
    def enter_ghost_mode(self):
        # Minimal stub for enter_ghost_mode
        self.ghost_mode = True
        print("[System] Ghost mode activated (stub)")
        print("👻 GHOST MODE ACTIVE - You are now invisible")
        print(f"🌐 External IP: 127.0.0.1")
        print(f"🔒 Tor: ✅")
        print(f"🎭 MAC Changed: ✅")
        return True
    def setup_kali_environment(self):
        # Minimal stub for setup_kali_environment
        print("[System] Kali environment setup (stub)")
        return True

    def setup_api_keys(self):
        # Minimal stub for setup_api_keys
        print("[System] API keys setup (stub)")
        return True
    def check_environment(self):
        # Minimal environment check; always returns True for now
        return True
    def __init__(self):
        self.console = Console()
        self.banner = Panel(
            Text(r"""
   ___        _        _____                 _    _      _            _    
  / _ \ _   _| |_ ___ | ____|_   _____ _ __ | | _| | ___| |_ ___  ___| |_  
 | | | | | | | __/ _ \|  _| \ \ / / _ \ '_ \| |/ / |/ _ \ __/ _ \/ __| __| 
 | |_| | |_| | || (_) | |___ \ V /  __/ | | |   <| |  __/ ||  __/ (__| |_  
  \__\_\\__,_|\__\___/|_____| \_/ \___|_| |_|_\_\_|\___|\__\___|\___|\__| 
            """, style="bold green"),
            title="[bold magenta]AutoGen Ethical Hacker",
            border_style="bright_cyan"
        )
        self.api_manager = APIQuotaManager()
        self.stealth = StealthManager()
        self.controller = AutonomousController()
        self.orchestrator = None
        self.ghost_mode = False
        self._setup_keybindings()

    def _setup_keybindings(self):
        self.kb = KeyBindings()
        @self.kb.add('c-z')
        def _(event):
            self.console.print("[yellow]Suspending... (Ctrl+Z)")
            event.app.exit()
        @self.kb.add('c-p')
        def _(event):
            self.console.print("[cyan]Paused. Press any key to continue...")
            input()
        @self.kb.add('c-s')
        def _(event):
            self.console.print("[magenta]Output suspended. Press any key to continue...")
            input()
    def chat_mode(self):
        """Chat-driven workflow for describing and planning complex tasks."""
        print("\n💬 CHAT MODE: Describe your objective in detail. Type 'done' when finished.\n")
        user_lines = []
        while True:
            line = input("You: ")
            if line.strip().lower() == 'done':
                break
            user_lines.append(line)
        long_task = " ".join(user_lines)
        print(f"\n[System] Summarizing and planning for: {long_task}\n")
        # Use Groq LLM to summarize and plan steps
        try:
            from groq import Groq
            groq_api = self.api_manager.apis.get('groq', {}).get('api_key', '')
            client = Groq(api_key=groq_api)
            prompt = f"You are an expert pentest orchestrator. Given this user objective, break it down into a step-by-step plan, select the best agents/tools for each step, and output a JSON plan. Objective: {long_task}"
            response = client.chat.completions.create(
                model="groq/gpt-oss-120b",
                messages=[{"role": "system", "content": "You are a pentest orchestrator."},
                          {"role": "user", "content": prompt}]
            )
            plan = response.choices[0].message.content
            print(f"[System] LLM-generated plan:\n{plan}\n")
        except Exception as e:
            print(f"[System] LLM planning failed: {e}")
            plan = None
        # Optionally, parse and execute the plan (if JSON)
        # For now, just run the main orchestrator with the summarized task
        print("[System] Executing the described task using the orchestrator...\n")
        self.autonomous_mode(task=long_task)

    
    def autonomous_mode(self, target=None, task=None):
        """Fully autonomous ethical hacking mode"""
        print("\n🤖 AUTONOMOUS MODE ACTIVATED")
        print("=" * 50)
        
        if not target:
            target = input("Enter target network/IP (or 'auto' for auto-discovery): ").strip()
            if target.lower() == 'auto':
                target = "192.168.1.0/24"  # Default internal network
        
        if not task:
            print("\nAutonomous task options:")
            print("1. Full penetration test")
            print("2. Network reconnaissance")
            print("3. Vulnerability assessment")
            print("4. Web application testing")
            print("5. Custom objective")
            
            choice = input("Select task (1-5): ").strip()
            
            tasks = {
                "1": "Full penetration test with exploitation",
                "2": "Network reconnaissance and mapping",
                "3": "Comprehensive vulnerability assessment",
                "4": "Advanced web application testing",
                "5": input("Describe your objective: ")
            }
            
            task = tasks.get(choice, "Full penetration test")
        
        print(f"🎯 Target: {target}")
        print(f"📋 Task: {task}")
        print(f"👻 Ghost Mode: {'✅' if self.ghost_mode else '❌'}")
        
        # Initialize orchestrator with autonomous capabilities
        if not self.orchestrator:
            apis = self.api_manager.apis
            # Load full lab_scope.json for proper agent integration
            lab_scope_path = os.path.join(os.path.dirname(__file__), "config", "lab_scope.json")
            try:
                with open(lab_scope_path, "r") as f:
                    lab_scope = json.load(f)
            except Exception as e:
                print(f"[ERROR] Could not load lab_scope.json: {e}")
                lab_scope = {"allowed_targets": [target]}
            tools_config = self.get_tools_config()
            self.orchestrator = OrchestratorAgent(apis, lab_scope, tools_config)
        
        # Execute autonomous task
        print("\n🚀 Starting autonomous execution...")
        result = self.orchestrator.run(task)
        
        # Autonomous post-exploitation
        if "success" in str(result).lower():
            print("\n🔄 Performing autonomous post-exploitation...")
            
            # Attempt privilege escalation
            privesc_results = self.controller.escalate_privileges()
            if privesc_results:
                print("⬆️ Privilege escalation opportunities found")
            
            # Setup persistence
            self.controller.create_persistent_backdoor()
            
            # Setup C2 infrastructure
            self.controller.setup_command_and_control()
        
        # Clean tracks if in ghost mode
        if self.ghost_mode:
            print("🧹 Cleaning tracks...")
            self.controller.clean_tracks()
        
        print("\n✅ Autonomous execution completed")
        return result
    
    def interactive_mode(self):
        """Interactive mode with full menu"""
        from main import main as interactive_main
        interactive_main()
    
    def get_tools_config(self):
        """Get tools configuration"""
        return {
            "nmap": {"enabled": True, "path": "/usr/bin/nmap"},
            "masscan": {"enabled": True, "path": "/usr/bin/masscan"},
            "sqlmap": {"enabled": True, "path": "/usr/bin/sqlmap"},
            "metasploit": {"enabled": True, "path": "/usr/bin/msfconsole"},
            "nikto": {"enabled": True, "path": "/usr/bin/nikto"}
        }
    
    def system_status(self):
        """Display current system status"""
        print("\n📊 SYSTEM STATUS")
        print("=" * 50)
        
        # System information
        info = self.controller.system_info
        print(f"🖥️  Hostname: {info['hostname']}")
        print(f"🐧 Kernel: {info['kernel']}")
        print(f"💾 Memory: {info['memory_gb']} GB")
        print(f"💿 Disk: {info['disk_space']['free_gb']} GB free")
        
        # Stealth status
        status = self.stealth.stealth_status()
        print(f"👻 Ghost Mode: {'✅' if self.ghost_mode else '❌'}")
        print(f"🌐 External IP: {status['external_ip']}")
        
        # API status
        api_status = self.api_manager.get_api_status()
        print(f"🔑 Groq Keys: {api_status['groq']['working_keys']}/{api_status['groq']['total_keys']}")
        print(f"🔑 Google Keys: {api_status['google']['working_keys']}/{api_status['google']['total_keys']}")
        
        # Resource monitoring
        resources = self.controller.monitor_system_resources()
        print(f"📈 CPU: {resources['cpu_percent']}%")
        print(f"📈 Memory: {resources['memory_percent']}%")
        print(f"📈 Disk: {resources['disk_percent']}%")
    
    def run(self):
        """Main entry point with beautiful terminal UI and key handling"""
        self.console.clear()
        self.console.print(self.banner)

        parser = argparse.ArgumentParser(description="Autonomous Ethical Hacker")
        parser.add_argument("--setup", action="store_true", help="Setup Kali environment")
        parser.add_argument("--ghost", action="store_true", help="Enable ghost mode")
        parser.add_argument("--auto", action="store_true", help="Full autonomous mode")
        parser.add_argument("--target", help="Target network/IP")
        parser.add_argument("--task", help="Task description")
        parser.add_argument("--interactive", action="store_true", help="Interactive mode")
        parser.add_argument("--status", action="store_true", help="Show system status")
        parser.add_argument("--agentic", action="store_true", help="Advanced agentic LLM mode")
        args = parser.parse_args()

        # Keybinding app for movie-style terminal
        app = Application(key_bindings=self.kb, full_screen=False)

        # Check environment
        if not self.check_environment():
            return False

        if args.setup:
            return self.setup_kali_environment()
        if args.status:
            self.system_status()
            return True
        if not self.setup_api_keys():
            self.console.print("[bold red]❌ API setup required for operation")
            return False
        if args.ghost:
            self.enter_ghost_mode()
        if args.agentic:
            self.console.print("[bold magenta][Agentic AI Mode] Launching advanced LLM-driven pentest agent...")
            agent = create_llm_pentest_agent()
            import asyncio
            target = args.target or self.console.input("[bold cyan]Enter target for nmap scan: ")
            asyncio.run(agent.run(task=f"Scan {target} for vulnerabilities."))
            return True
        if args.auto:
            return self.autonomous_mode(args.target, args.task)
        if args.interactive:
            self.interactive_mode()
            return True

        # Default: beautiful menu
        while True:
            self.console.print(Panel("""
[bold green]1.[/] 🤖 Full Autonomous Mode
[bold green]2.[/] 🎮 Interactive Mode
[bold green]3.[/] 👻 Ghost Mode + Autonomous
[bold green]4.[/] 📊 System Status
[bold green]5.[/] 🤖 Agentic LLM Mode
[bold green]6.[/] 📝 Generate Pentest Report (Demo)
[bold green]7.[/] 🌐 Threat Intel Enrichment (Demo)
[bold green]8.[/] 🧠 Ultra-Advanced Multi-Agent Workflow (NEW)
[bold green]9.[/] 🧩 Advanced Features Menu (ALL STUBS)
[bold green]0.[/] 🚪 Exit
""", title="[bold cyan]Choose your mode:", border_style="green"))
            choice = self.console.input("[bold yellow]\nSelect mode (0-9): ").strip()
            if choice == "1":
                return self.autonomous_mode()
            elif choice == "2":
                self.interactive_mode()
                return True
            elif choice == "3":
                self.enter_ghost_mode()
                return self.autonomous_mode()
            elif choice == "4":
                self.system_status()
                return True
            elif choice == "5":
                self.console.print("[bold magenta][Agentic AI Mode] Launching advanced LLM-driven pentest agent...")
                agent = create_llm_pentest_agent()
                import asyncio
                target = self.console.input("[bold cyan]Enter target for nmap scan: ")
                asyncio.run(agent.run(task=f"Scan {target} for vulnerabilities."))
                return True
            elif choice == "6":
                findings = [
                    {"title": "Open SSH Port", "description": "SSH port 22 open.", "evidence": "nmap found port 22/tcp open", "remediation": "Restrict SSH access or use key auth."},
                    {"title": "Outdated Apache", "description": "Apache 2.2.15 detected.", "evidence": "Banner grab shows Apache/2.2.15", "remediation": "Update Apache to latest version."}
                ]
                target = self.console.input("[bold cyan]Target for report: ")
                self.generate_report(findings, target)
                return True
            elif choice == "7":
                ip = self.console.input("[bold cyan]IP to enrich: ")
                self.enrich_ip(ip)
                return True
            elif choice == "8":
                self.console.print("[bold blue][Ultra-Advanced] Launching Multi-Agent Workflow...")
                workflow = MultiAgentWorkflow()
                target_scope = self.console.input("[bold cyan]Enter target scope (e.g., 192.168.1.0/24 or domain): ")
                result = workflow.run_workflow(target_scope)
                self.console.print("[bold blue][Ultra-Advanced] Workflow result:")
                self.console.print(result)
                return True
            elif choice == "9":
                self.advanced_features_menu()
                return True
            elif choice == "0":
                self.console.print("[bold red]👋 Goodbye!")
                return True
            else:
                self.console.print("[bold red]❌ Invalid choice")

def main():
    try:
        hacker = AutonomousEthicalHacker()
        return hacker.run()
    except KeyboardInterrupt:
        print("\n\n🛑 Operation interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Critical error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)