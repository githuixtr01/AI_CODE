#!/usr/bin/env python3
"""
🚀 Enhanced AI_CODE Ethical Hacker with Robust Self-Healing
Complete autonomous penetration testing platform with advanced recovery capabilities
"""

import os
import sys
from pathlib import Path
import time
import json
from datetime import datetime

# Set API keys in environment
os.environ["GROQ_API_KEY"] = "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"
os.environ["GOOGLE_API_KEY"] = "AIzaSyCbIDV8wJ-3TL8BtI_HPdWVUSClBgoRszM"

# Add project root to path
sys.path.append(str(Path(__file__).parent))

# Import self-healing components
from system.self_healing_manager import self_healing_manager
from llm.enhanced_llm_router import enhanced_llm_router
from tools.enhanced_tool_wrapper import enhanced_tool_wrapper

class EnhancedEthicalHacker:
    """
    Enhanced Ethical Hacker with comprehensive self-healing capabilities
    """
    
    def __init__(self):
        self.banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🚀 AI_CODE ETHICAL HACKER - ENHANCED                      ║
║                      🔄 SELF-HEALING EDITION 🔄                             ║
║               AI-Powered Penetration Testing with Auto-Recovery              ║
║                                                                              ║
║  ✅ Robust Self-Healing    ✅ API Failover & Recovery                       ║
║  ✅ Tool Auto-Repair       ✅ Intelligent Retry Logic                       ║
║  ✅ Health Monitoring      ✅ Emergency Recovery Mode                       ║
║  ✅ Circuit Breakers       ✅ Comprehensive Diagnostics                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
        
        # Initialize self-healing systems
        self.initialize_self_healing()
        
        # Load configurations with auto-repair
        self.load_configurations()
        
        # Start continuous monitoring
        self.start_monitoring()
    
    def initialize_self_healing(self):
        """Initialize all self-healing components"""
        print("🔄 Initializing self-healing systems...")
        
        # Perform initial health check
        health_report = self_healing_manager.perform_comprehensive_health_check()
        
        if health_report['overall_status'] != 'healthy':
            print("⚠️ System health issues detected, performing auto-healing...")
            self_healing_manager.perform_auto_healing()
        
        # Start continuous monitoring (every 5 minutes)
        self_healing_manager.start_continuous_monitoring(interval=300)
        
        print("✅ Self-healing systems initialized")
    
    def load_configurations(self):
        """Load configurations with auto-repair if corrupted"""
        try:
            # Ensure config files exist and are valid
            if not self_healing_manager.check_config_files():
                print("🔧 Repairing configuration files...")
                self_healing_manager.auto_repair_config_files()
            
            # Load lab scope
            try:
                with open('config/lab_scope.json', 'r') as f:
                    self.lab_scope = json.load(f)
            except:
                self.lab_scope = {"allowed_targets": ["127.0.0.1", "192.168.1.0/24"]}
            
            # Load tools config  
            try:
                with open('config/tools_config.json', 'r') as f:
                    self.tools_config = json.load(f)
            except:
                self.tools_config = {"nmap_path": "nmap", "sqlmap_path": "sqlmap"}
                
            print("✅ Configurations loaded successfully")
            
        except Exception as e:
            print(f"⚠️ Configuration loading error: {e}")
            print("🔧 Using default configurations...")
            self.lab_scope = {"allowed_targets": ["127.0.0.1", "192.168.1.0/24"]}
            self.tools_config = {"nmap_path": "nmap", "sqlmap_path": "sqlmap"}
    
    def start_monitoring(self):
        """Start health monitoring for all components"""
        print("🩺 Starting comprehensive health monitoring...")
        
        # Initial health checks
        llm_health = enhanced_llm_router.health_check()
        tool_health = enhanced_tool_wrapper.health_check_all_tools()
        
        print(f"🤖 LLM Health: {llm_health['overall_health']}")
        print(f"🛠️ Tools Health: {tool_health['overall_health']}")
    
    def display_banner(self):
        print(self.banner)
    
    def display_menu(self):
        print("""
🎯 ENHANCED PENETRATION TESTING OPERATIONS:

1.  🔍 Network Reconnaissance (Enhanced Nmap)
2.  🌐 Web Vulnerability Testing (Enhanced SQLMap)
3.  🔒 Web Server Analysis (Enhanced Nikto)
4.  ⚡ Fast Port Scanning (Enhanced Masscan)
5.  🤖 AI Analysis with Auto-Failover
6.  📊 System Health & Status
7.  🔄 Self-Healing Operations
8.  👻 Ghost Mode Operations
9.  🎲 Custom Task with AI Planning
10. 🚨 Emergency Recovery Mode
0.  🚪 Exit
        """)
    
    def enhanced_reconnaissance(self, target=None):
        """Enhanced network reconnaissance with self-healing"""
        if not target:
            target = input("Enter target IP/hostname: ").strip()
        
        if not self.validate_target(target):
            print("❌ Target not in allowed scope!")
            return None
        
        print(f"🔍 Running enhanced Nmap scan on {target}...")
        results = enhanced_tool_wrapper.enhanced_nmap([target])
        print("✅ Enhanced Nmap scan completed")
        return results
    
    def enhanced_web_testing(self, target=None):
        """Enhanced web vulnerability testing with self-healing"""
        if not target:
            target = input("Enter target URL: ").strip()
        
        print(f"🌐 Running enhanced SQLMap on {target}...")
        results = enhanced_tool_wrapper.enhanced_sqlmap(target, ["--batch", "--level=1", "--risk=1"])
        print("✅ Enhanced SQLMap scan completed")
        return results
    
    def enhanced_web_analysis(self, target=None):
        """Enhanced web server analysis with self-healing"""
        if not target:
            target = input("Enter target URL: ").strip()
        
        print(f"🔒 Running enhanced Nikto on {target}...")
        results = enhanced_tool_wrapper.enhanced_nikto(target, ["-C", "all"])
        print("✅ Enhanced Nikto scan completed")
        return results
    
    def enhanced_port_scan(self, target=None):
        """Enhanced port scanning with self-healing"""
        if not target:
            target = input("Enter target IP: ").strip()
        
        if not self.validate_target(target):
            print("❌ Target not in allowed scope!")
            return None
        
        print(f"⚡ Running enhanced Masscan on {target}...")
        results = enhanced_tool_wrapper.enhanced_masscan([target], "1-1000")
        print("✅ Enhanced Masscan completed")
        return results
    
    def ai_analysis_with_failover(self):
        """AI analysis with automatic failover and retry"""
        print("🤖 AI Analysis Mode with Auto-Failover")
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
        
        print("🤖 Analyzing with enhanced AI (auto-failover enabled)...")
        result = enhanced_llm_router.llm_complete(prompt)
        
        print("🤖 Enhanced AI Analysis Results:")
        print("-" * 60)
        print(result)
        print("-" * 60)
        
        return result
    
    def system_health_status(self):
        """Comprehensive system health and status check"""
        print("\n📊 ENHANCED SYSTEM HEALTH & STATUS")
        print("=" * 80)
        
        # API Health
        api_health = enhanced_llm_router.health_check()
        print(f"🤖 LLM APIs Health: {api_health['overall_health'].upper()}")
        for provider, status in api_health['providers'].items():
            emoji = "✅" if status['healthy'] else "❌"
            print(f"  {emoji} {provider.title()}: {status.get('response_time', 'N/A')}s response time")
        
        # Tools Health
        tool_health = enhanced_tool_wrapper.health_check_all_tools()
        print(f"\n🛠️ Security Tools Health: {tool_health['overall_health'].upper()}")
        for tool, status in tool_health['tools'].items():
            emoji = "✅" if status['healthy'] else "❌"
            failures = status['failures']
            print(f"  {emoji} {tool}: {failures} failures")
        
        # Self-Healing Status
        healing_status = self_healing_manager.get_healing_status()
        print(f"\n🔄 Self-Healing: {'✅ ENABLED' if healing_status['enabled'] else '❌ DISABLED'}")
        print(f"📅 Last Health Check: {healing_status['last_health_check']}")
        
        # Recent Healing Activities
        recent_activities = healing_status['recent_healing_log'][-5:]
        if recent_activities:
            print("\n📋 Recent Self-Healing Activities:")
            for activity in recent_activities:
                print(f"  • {activity}")
        
        # System Info
        import platform
        print(f"\n🖥️  System: {platform.system()} {platform.release()}")
        print(f"🐍 Python: {platform.python_version()}")
        
        return True
    
    def self_healing_operations(self):
        """Manual self-healing operations menu"""
        print("\n🔄 SELF-HEALING OPERATIONS")
        print("=" * 60)
        print("1. 🩺 Perform Health Check")
        print("2. 🔧 Run Auto-Healing")
        print("3. 🔄 Reset Circuit Breakers")
        print("4. 🛠️ Repair All Tools")
        print("5. 📊 View Healing Status")
        print("6. 🚨 Emergency Recovery")
        print("0. ← Back to Main Menu")
        
        choice = input("\n🔄 Select healing operation: ").strip()
        
        if choice == "1":
            print("🩺 Performing comprehensive health check...")
            health_report = self_healing_manager.perform_comprehensive_health_check()
            print(f"Overall Status: {health_report['overall_status'].upper()}")
            if health_report['failed_components']:
                print(f"Failed Components: {health_report['failed_components']}")
        
        elif choice == "2":
            print("🔧 Running auto-healing...")
            success = self_healing_manager.perform_auto_healing()
            if success:
                print("✅ Auto-healing completed successfully")
            else:
                print("⚠️ Auto-healing completed with some issues")
        
        elif choice == "3":
            print("🔄 Resetting circuit breakers...")
            enhanced_llm_router.reset_circuit_breakers()
            print("✅ Circuit breakers reset")
        
        elif choice == "4":
            print("🛠️ Repairing all tools...")
            success = enhanced_tool_wrapper.auto_repair_all_tools()
            if success:
                print("✅ All tools repaired successfully")
            else:
                print("⚠️ Some tool repairs failed")
        
        elif choice == "5":
            print("📊 Current healing status:")
            status = self_healing_manager.get_healing_status()
            print(json.dumps(status, indent=2, default=str))
        
        elif choice == "6":
            print("🚨 EMERGENCY RECOVERY MODE")
            confirm = input("This will aggressively attempt to repair all systems. Continue? (y/N): ")
            if confirm.lower() == 'y':
                success = self_healing_manager.emergency_recovery()
                if success:
                    print("✅ Emergency recovery successful")
                else:
                    print("❌ Emergency recovery incomplete")
        
        return True
    
    def validate_target(self, target):
        """Validate target against allowed scope"""
        allowed = self.lab_scope.get("allowed_targets", [])
        return any(target.startswith(allowed_target.split('/')[0]) for allowed_target in allowed)
    
    def ghost_mode(self):
        """Enhanced ghost mode with self-healing"""
        print("👻 ENHANCED GHOST MODE OPERATIONS")
        print("=" * 60)
        
        # Check stealth capabilities
        try:
            from system.stealth_manager import StealthManager
            stealth_manager = StealthManager()
            status = stealth_manager.stealth_status()
            print(f"🌐 External IP: {status['external_ip']}")
            print(f"👻 Ghost Mode: {status.get('stealth_level', 'Normal')}")
            print("🔒 Enhanced anonymization with self-healing enabled")
        except Exception as e:
            print("👻 Ghost Mode: Basic stealth features available")
            print("🔒 Advanced features require proper dependencies")
            print(f"ℹ️ Note: {e}")
        
        return True
    
    def custom_task_with_ai(self):
        """Custom task planning with enhanced AI"""
        print("🎲 ENHANCED CUSTOM TASK MODE")
        task_description = input("Describe your penetration testing objective: ").strip()
        
        prompt = f"""
        You are a penetration testing expert with self-healing capabilities. Create a comprehensive step-by-step plan for this objective:
        
        {task_description}
        
        Provide a detailed methodology with:
        1. Reconnaissance steps with failover options
        2. Vulnerability identification with multiple tools
        3. Exploitation techniques with retry mechanisms
        4. Post-exploitation activities with cleanup
        5. Reporting requirements
        6. Self-healing considerations for each phase
        """
        
        print("🤖 Creating enhanced penetration testing plan with AI failover...")
        plan = enhanced_llm_router.llm_complete(prompt)
        
        print("🎲 Enhanced Custom Task Plan:")
        print("-" * 60)
        print(plan)
        print("-" * 60)
        
        execute = input("Execute this plan with self-healing enabled? (y/n): ").strip().lower()
        if execute == 'y':
            print("⚠️ Enhanced execution would require additional implementation")
            print("🔄 Self-healing monitoring enabled for manual execution")
        
        return plan
    
    def emergency_recovery_mode(self):
        """Emergency recovery mode for critical failures"""
        print("🚨 EMERGENCY RECOVERY MODE")
        print("=" * 60)
        print("⚠️ This mode will attempt aggressive recovery of all systems")
        print("🔧 It may take several minutes and restart workflows")
        
        confirm = input("Continue with emergency recovery? (y/N): ").strip().lower()
        if confirm != 'y':
            print("❌ Emergency recovery cancelled")
            return False
        
        print("🚨 Starting emergency recovery...")
        success = self_healing_manager.emergency_recovery()
        
        if success:
            print("✅ Emergency recovery completed successfully!")
            print("🔄 All systems should now be operational")
        else:
            print("❌ Emergency recovery incomplete")
            print("📞 Manual intervention may be required")
        
        return success
    
    def run(self):
        """Enhanced main application loop with self-healing"""
        self.display_banner()
        
        # Perform initial system check
        print("🔄 Performing initial system health check...")
        health_report = self_healing_manager.perform_comprehensive_health_check()
        
        if health_report['overall_status'] == 'healthy':
            print("✅ All systems healthy and ready")
        else:
            print("⚠️ Some systems need attention - auto-healing in progress...")
            self_healing_manager.perform_auto_healing()
        
        while True:
            try:
                self.display_menu()
                choice = input("\n🎯 Select enhanced operation (0-10): ").strip()
                
                print()  # Add spacing
                
                if choice == "1":
                    self.enhanced_reconnaissance()
                elif choice == "2":
                    self.enhanced_web_testing()
                elif choice == "3":
                    self.enhanced_web_analysis()
                elif choice == "4":
                    self.enhanced_port_scan()
                elif choice == "5":
                    self.ai_analysis_with_failover()
                elif choice == "6":
                    self.system_health_status()
                elif choice == "7":
                    self.self_healing_operations()
                elif choice == "8":
                    self.ghost_mode()
                elif choice == "9":
                    self.custom_task_with_ai()
                elif choice == "10":
                    self.emergency_recovery_mode()
                elif choice == "0":
                    print("👋 Goodbye! Enhanced systems shutting down safely...")
                    self_healing_manager.stop_monitoring()
                    break
                else:
                    print("❌ Invalid choice. Please try again.")
                
                input("\nPress Enter to continue...")
                print("\n" + "="*80 + "\n")
                
            except KeyboardInterrupt:
                print("\n\n🛑 Operation interrupted - performing safe shutdown...")
                self_healing_manager.stop_monitoring()
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                print("🔄 Self-healing systems attempting recovery...")
                try:
                    self_healing_manager.perform_auto_healing()
                except:
                    pass

def main():
    """Main entry point for enhanced ethical hacker"""
    try:
        print("""
🚀 AI_CODE ETHICAL HACKER - ENHANCED SELF-HEALING EDITION
========================================================
Starting advanced penetration testing platform with:
✅ Robust self-healing capabilities
✅ API failover and recovery  
✅ Tool auto-repair
✅ Intelligent retry mechanisms
✅ Health monitoring
✅ Emergency recovery mode
        """)
        
        hacker = EnhancedEthicalHacker()
        hacker.run()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Enhanced platform shutdown requested")
    except Exception as e:
        print(f"\n❌ Critical platform error: {e}")
        print("🚨 Attempting emergency recovery...")
        
        try:
            from system.self_healing_manager import self_healing_manager
            self_healing_manager.emergency_recovery()
        except:
            print("❌ Emergency recovery failed - manual intervention required")

if __name__ == "__main__":
    main()