#!/usr/bin/env python3
"""
🔄 Self-Healing Manager for AI_CODE Ethical Hacker Platform
Automatically detects and recovers from various system failures
"""

import os
import sys
import time
import json
import subprocess
import threading
import traceback
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
import logging

class SelfHealingManager:
    """
    Comprehensive self-healing system that monitors and repairs platform components
    """
    
    def __init__(self):
        self.healing_log = []
        self.component_status = {}
        self.retry_configs = {
            'api_calls': {'max_retries': 3, 'base_delay': 1, 'max_delay': 30},
            'tool_execution': {'max_retries': 2, 'base_delay': 2, 'max_delay': 60},
            'dependency_install': {'max_retries': 3, 'base_delay': 5, 'max_delay': 120}
        }
        self.monitoring_enabled = True
        self.auto_healing_enabled = True
        
        # Setup logging
        self.setup_logging()
        
        # Initialize component monitors
        self.initialize_monitors()
        
        self.log_healing("🔄 Self-Healing Manager initialized")
    
    def setup_logging(self):
        """Setup detailed logging for self-healing activities"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'self_healing.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def initialize_monitors(self):
        """Initialize monitoring for all system components"""
        self.components = {
            'api_groq': {'status': 'unknown', 'last_check': None, 'failures': 0},
            'api_google': {'status': 'unknown', 'last_check': None, 'failures': 0},
            'tool_nmap': {'status': 'unknown', 'last_check': None, 'failures': 0},
            'tool_sqlmap': {'status': 'unknown', 'last_check': None, 'failures': 0},
            'tool_nikto': {'status': 'unknown', 'last_check': None, 'failures': 0},
            'tool_masscan': {'status': 'unknown', 'last_check': None, 'failures': 0},
            'dependencies': {'status': 'unknown', 'last_check': None, 'failures': 0},
            'config_files': {'status': 'unknown', 'last_check': None, 'failures': 0}
        }
    
    def log_healing(self, message: str, level: str = "INFO"):
        """Log healing activities with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        self.healing_log.append(log_entry)
        
        if level == "ERROR":
            self.logger.error(message)
        elif level == "WARNING":
            self.logger.warning(message)
        else:
            self.logger.info(message)
        
        # Keep only last 1000 entries
        if len(self.healing_log) > 1000:
            self.healing_log = self.healing_log[-1000:]
    
    def exponential_backoff_retry(self, func: Callable, component_type: str, *args, **kwargs) -> Any:
        """Execute function with exponential backoff retry"""
        config = self.retry_configs.get(component_type, self.retry_configs['api_calls'])
        max_retries = config['max_retries']
        base_delay = config['base_delay']
        max_delay = config['max_delay']
        
        for attempt in range(max_retries + 1):
            try:
                result = func(*args, **kwargs)
                if attempt > 0:
                    self.log_healing(f"✅ Recovery successful after {attempt} attempts for {func.__name__}")
                return result
            except Exception as e:
                if attempt == max_retries:
                    self.log_healing(f"❌ All retry attempts failed for {func.__name__}: {str(e)}", "ERROR")
                    raise e
                
                delay = min(base_delay * (2 ** attempt), max_delay)
                self.log_healing(f"⚠️ Attempt {attempt + 1} failed for {func.__name__}, retrying in {delay}s: {str(e)}", "WARNING")
                time.sleep(delay)
    
    def check_api_health(self) -> Dict[str, bool]:
        """Check health of API providers"""
        api_status = {}
        
        # Check Groq API
        try:
            from llm.simple_llm_router import llm_complete
            result = self.exponential_backoff_retry(
                llm_complete, 'api_calls',
                "Health check", provider="groq", max_tokens=10
            )
            api_status['groq'] = "error" not in result.lower()
            self.components['api_groq']['status'] = 'healthy' if api_status['groq'] else 'failed'
            self.components['api_groq']['failures'] = 0 if api_status['groq'] else self.components['api_groq']['failures'] + 1
        except Exception as e:
            api_status['groq'] = False
            self.components['api_groq']['status'] = 'failed'
            self.components['api_groq']['failures'] += 1
            self.log_healing(f"🔴 Groq API health check failed: {str(e)}", "ERROR")
        
        # Check Google API
        try:
            from llm.simple_llm_router import llm_complete
            result = self.exponential_backoff_retry(
                llm_complete, 'api_calls',
                "Health check", provider="google", max_tokens=10
            )
            api_status['google'] = "error" not in result.lower()
            self.components['api_google']['status'] = 'healthy' if api_status['google'] else 'failed'
            self.components['api_google']['failures'] = 0 if api_status['google'] else self.components['api_google']['failures'] + 1
        except Exception as e:
            api_status['google'] = False
            self.components['api_google']['status'] = 'failed'
            self.components['api_google']['failures'] += 1
            self.log_healing(f"🔴 Google API health check failed: {str(e)}", "ERROR")
        
        self.components['api_groq']['last_check'] = datetime.now()
        self.components['api_google']['last_check'] = datetime.now()
        
        return api_status
    
    def check_tools_health(self) -> Dict[str, bool]:
        """Check health of security tools"""
        tools_status = {}
        
        tools_to_check = {
            'nmap': 'nmap --version',
            'sqlmap': 'sqlmap --version',
            'nikto': 'nikto -Version',
            'masscan': 'masscan --version'
        }
        
        for tool_name, command in tools_to_check.items():
            try:
                result = subprocess.run(
                    command.split(), 
                    capture_output=True, 
                    timeout=10,
                    text=True
                )
                tools_status[tool_name] = result.returncode == 0
                component_key = f'tool_{tool_name}'
                self.components[component_key]['status'] = 'healthy' if tools_status[tool_name] else 'failed'
                self.components[component_key]['failures'] = 0 if tools_status[tool_name] else self.components[component_key]['failures'] + 1
                self.components[component_key]['last_check'] = datetime.now()
                
                if not tools_status[tool_name]:
                    self.log_healing(f"🔴 Tool {tool_name} health check failed", "WARNING")
                    
            except Exception as e:
                tools_status[tool_name] = False
                component_key = f'tool_{tool_name}'
                self.components[component_key]['status'] = 'failed'
                self.components[component_key]['failures'] += 1
                self.components[component_key]['last_check'] = datetime.now()
                self.log_healing(f"🔴 Tool {tool_name} check error: {str(e)}", "ERROR")
        
        return tools_status
    
    def auto_repair_tools(self) -> bool:
        """Attempt to automatically repair failed tools"""
        tools_status = self.check_tools_health()
        repair_success = True
        
        failed_tools = [tool for tool, status in tools_status.items() if not status]
        
        if failed_tools:
            self.log_healing(f"🔧 Attempting to repair failed tools: {failed_tools}")
            
            for tool in failed_tools:
                try:
                    self.log_healing(f"🔧 Installing {tool}...")
                    result = subprocess.run(
                        ['nix-env', '-iA', f'nixpkgs.{tool}'], 
                        capture_output=True, 
                        timeout=120,
                        text=True
                    )
                    
                    if result.returncode == 0:
                        self.log_healing(f"✅ Successfully repaired {tool}")
                    else:
                        self.log_healing(f"❌ Failed to repair {tool}: {result.stderr}", "ERROR")
                        repair_success = False
                        
                except Exception as e:
                    self.log_healing(f"❌ Error repairing {tool}: {str(e)}", "ERROR")
                    repair_success = False
        
        return repair_success
    
    def check_dependencies(self) -> bool:
        """Check if all required Python dependencies are available"""
        required_modules = [
            'groq', 'google.generativeai', 'rich', 'prompt_toolkit',
            'requests', 'pyyaml', 'networkx', 'matplotlib'
        ]
        
        missing_modules = []
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                missing_modules.append(module)
        
        if missing_modules:
            self.log_healing(f"🔴 Missing dependencies: {missing_modules}", "WARNING")
            self.components['dependencies']['status'] = 'failed'
            self.components['dependencies']['failures'] += 1
            return False
        else:
            self.components['dependencies']['status'] = 'healthy'
            self.components['dependencies']['failures'] = 0
            return True
    
    def auto_repair_dependencies(self) -> bool:
        """Attempt to automatically repair missing dependencies"""
        self.log_healing("🔧 Checking and repairing dependencies...")
        
        try:
            # Try to reinstall key packages
            result = subprocess.run([
                'uv', 'add', 'groq', 'google-generativeai', 'rich', 'prompt-toolkit'
            ], capture_output=True, timeout=180, text=True)
            
            if result.returncode == 0:
                self.log_healing("✅ Dependencies repair successful")
                return True
            else:
                self.log_healing(f"❌ Dependencies repair failed: {result.stderr}", "ERROR")
                return False
                
        except Exception as e:
            self.log_healing(f"❌ Error repairing dependencies: {str(e)}", "ERROR")
            return False
    
    def check_config_files(self) -> bool:
        """Check if configuration files are valid"""
        config_files = [
            'config/lab_scope.json',
            'config/tools_config.json'
        ]
        
        all_valid = True
        for config_file in config_files:
            try:
                if os.path.exists(config_file):
                    with open(config_file, 'r') as f:
                        json.load(f)  # Validate JSON
                else:
                    self.log_healing(f"🔴 Missing config file: {config_file}", "WARNING")
                    all_valid = False
            except json.JSONDecodeError as e:
                self.log_healing(f"🔴 Invalid JSON in {config_file}: {str(e)}", "ERROR")
                all_valid = False
            except Exception as e:
                self.log_healing(f"🔴 Error checking {config_file}: {str(e)}", "ERROR")
                all_valid = False
        
        self.components['config_files']['status'] = 'healthy' if all_valid else 'failed'
        self.components['config_files']['failures'] = 0 if all_valid else self.components['config_files']['failures'] + 1
        self.components['config_files']['last_check'] = datetime.now()
        
        return all_valid
    
    def auto_repair_config_files(self) -> bool:
        """Attempt to automatically repair configuration files"""
        self.log_healing("🔧 Repairing configuration files...")
        
        try:
            # Ensure config directory exists
            os.makedirs('config', exist_ok=True)
            
            # Create default lab_scope.json if missing
            lab_scope_path = 'config/lab_scope.json'
            if not os.path.exists(lab_scope_path):
                default_lab_scope = {
                    "allowed_targets": ["127.0.0.1", "192.168.1.0/24", "10.0.0.0/24"],
                    "forbidden_targets": ["0.0.0.0/0"],
                    "max_scan_rate": "1000",
                    "timeout": "300"
                }
                with open(lab_scope_path, 'w') as f:
                    json.dump(default_lab_scope, f, indent=2)
                self.log_healing("✅ Created default lab_scope.json")
            
            # Create default tools_config.json if missing
            tools_config_path = 'config/tools_config.json'
            if not os.path.exists(tools_config_path):
                default_tools_config = {
                    "nmap_path": "nmap",
                    "sqlmap_path": "sqlmap",
                    "nikto_path": "nikto",
                    "masscan_path": "masscan",
                    "default_scan_options": {
                        "nmap": ["-sV", "-Pn"],
                        "sqlmap": ["--batch"],
                        "nikto": ["-C", "all"],
                        "masscan": ["--rate=1000"]
                    }
                }
                with open(tools_config_path, 'w') as f:
                    json.dump(default_tools_config, f, indent=2)
                self.log_healing("✅ Created default tools_config.json")
            
            return True
            
        except Exception as e:
            self.log_healing(f"❌ Error repairing config files: {str(e)}", "ERROR")
            return False
    
    def perform_comprehensive_health_check(self) -> Dict[str, Any]:
        """Perform comprehensive health check of all components"""
        self.log_healing("🩺 Performing comprehensive health check...")
        
        health_report = {
            'timestamp': datetime.now().isoformat(),
            'apis': self.check_api_health(),
            'tools': self.check_tools_health(),
            'dependencies': self.check_dependencies(),
            'config_files': self.check_config_files(),
            'overall_status': 'healthy'
        }
        
        # Determine overall status
        failed_components = []
        for category, status in health_report.items():
            if category == 'timestamp' or category == 'overall_status':
                continue
            
            if isinstance(status, dict):
                failed_items = [k for k, v in status.items() if not v]
                if failed_items:
                    failed_components.extend([f"{category}.{item}" for item in failed_items])
            elif not status:
                failed_components.append(category)
        
        if failed_components:
            health_report['overall_status'] = 'degraded'
            health_report['failed_components'] = failed_components
            self.log_healing(f"⚠️ System health degraded. Failed components: {failed_components}", "WARNING")
        else:
            health_report['failed_components'] = []
            self.log_healing("✅ All components healthy")
        
        return health_report
    
    def perform_auto_healing(self) -> bool:
        """Perform automatic healing of failed components"""
        if not self.auto_healing_enabled:
            return False
        
        self.log_healing("🔄 Starting auto-healing process...")
        
        health_report = self.perform_comprehensive_health_check()
        healing_success = True
        
        # Repair failed components
        if not health_report['dependencies']:
            if not self.auto_repair_dependencies():
                healing_success = False
        
        if not health_report['config_files']:
            if not self.auto_repair_config_files():
                healing_success = False
        
        # Repair failed tools
        failed_tools = [tool for tool, status in health_report['tools'].items() if not status]
        if failed_tools:
            if not self.auto_repair_tools():
                healing_success = False
        
        # API issues typically require manual intervention (API keys, quotas, etc.)
        failed_apis = [api for api, status in health_report['apis'].items() if not status]
        if failed_apis:
            self.log_healing(f"⚠️ API issues detected: {failed_apis}. Manual intervention may be required.", "WARNING")
        
        if healing_success:
            self.log_healing("✅ Auto-healing completed successfully")
        else:
            self.log_healing("⚠️ Auto-healing completed with some failures", "WARNING")
        
        return healing_success
    
    def get_healing_status(self) -> Dict[str, Any]:
        """Get current healing status and recent activities"""
        # Get last health check time safely
        last_checks = [comp.get('last_check') for comp in self.components.values() if comp.get('last_check')]
        last_health_check = max(last_checks) if last_checks else None
        
        return {
            'enabled': self.auto_healing_enabled,
            'last_health_check': last_health_check,
            'components': self.components,
            'recent_healing_log': self.healing_log[-20:],  # Last 20 entries
            'retry_configs': self.retry_configs
        }
    
    def emergency_recovery(self) -> bool:
        """Emergency recovery mode - aggressive healing attempts"""
        self.log_healing("🚨 EMERGENCY RECOVERY MODE ACTIVATED", "WARNING")
        
        try:
            # Force reinstall all tools
            tools = ['nmap', 'sqlmap', 'nikto', 'masscan']
            for tool in tools:
                try:
                    subprocess.run(['nix-env', '-e', tool], capture_output=True, timeout=30)
                    subprocess.run(['nix-env', '-iA', f'nixpkgs.{tool}'], capture_output=True, timeout=120)
                    self.log_healing(f"🔧 Emergency reinstall of {tool}")
                except:
                    pass
            
            # Force reinstall Python dependencies
            try:
                subprocess.run(['uv', 'sync'], capture_output=True, timeout=180)
                self.log_healing("🔧 Emergency sync of Python dependencies")
            except:
                pass
            
            # Recreate all config files
            self.auto_repair_config_files()
            
            # Final health check
            health_report = self.perform_comprehensive_health_check()
            
            if health_report['overall_status'] == 'healthy':
                self.log_healing("✅ Emergency recovery successful!")
                return True
            else:
                self.log_healing("❌ Emergency recovery incomplete", "ERROR")
                return False
                
        except Exception as e:
            self.log_healing(f"❌ Emergency recovery failed: {str(e)}", "ERROR")
            return False
    
    def start_continuous_monitoring(self, interval: int = 300):
        """Start continuous monitoring thread (interval in seconds)"""
        def monitor_loop():
            while self.monitoring_enabled:
                try:
                    health_report = self.perform_comprehensive_health_check()
                    
                    if health_report['overall_status'] == 'degraded':
                        self.perform_auto_healing()
                    
                    time.sleep(interval)
                    
                except Exception as e:
                    self.log_healing(f"❌ Monitoring loop error: {str(e)}", "ERROR")
                    time.sleep(60)  # Wait before retrying
        
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
        self.log_healing(f"🔄 Continuous monitoring started (interval: {interval}s)")
    
    def stop_monitoring(self):
        """Stop continuous monitoring"""
        self.monitoring_enabled = False
        self.log_healing("🛑 Continuous monitoring stopped")
    
    def __del__(self):
        """Cleanup when object is destroyed"""
        self.stop_monitoring()

# Global instance for easy access
self_healing_manager = SelfHealingManager()