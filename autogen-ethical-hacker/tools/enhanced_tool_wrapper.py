#!/usr/bin/env python3
"""
🔧 Enhanced Tool Wrapper with Self-Healing Capabilities
Provides robust tool execution, auto-recovery, and failure handling
"""

import os
import subprocess
import time
import logging
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
from pathlib import Path

class EnhancedToolWrapper:
    """
    Self-healing wrapper for security tools with automatic recovery
    """
    
    def __init__(self):
        self.tool_status = {}
        self.setup_logging()
        self.initialize_tools()
    
    def setup_logging(self):
        """Setup logging for tool operations"""
        self.logger = logging.getLogger('EnhancedToolWrapper')
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def initialize_tools(self):
        """Initialize tool status tracking"""
        self.tools = {
            'nmap': {
                'command': 'nmap',
                'version_flag': '--version',
                'install_command': ['nix-env', '-iA', 'nixpkgs.nmap'],
                'status': 'unknown',
                'last_success': None,
                'failures': 0
            },
            'sqlmap': {
                'command': 'sqlmap',
                'version_flag': '--version',
                'install_command': ['nix-env', '-iA', 'nixpkgs.sqlmap'],
                'status': 'unknown',
                'last_success': None,
                'failures': 0
            },
            'nikto': {
                'command': 'nikto',
                'version_flag': '-Version',
                'install_command': ['nix-env', '-iA', 'nixpkgs.nikto'],
                'status': 'unknown',
                'last_success': None,
                'failures': 0
            },
            'masscan': {
                'command': 'masscan',
                'version_flag': '--version',
                'install_command': ['nix-env', '-iA', 'nixpkgs.masscan'],
                'status': 'unknown',
                'last_success': None,
                'failures': 0
            }
        }
    
    def _check_tool_availability(self, tool_name: str) -> bool:
        """Check if a tool is available and working"""
        if tool_name not in self.tools:
            return False
        
        tool_config = self.tools[tool_name]
        
        try:
            result = subprocess.run(
                [tool_config['command'], tool_config['version_flag']],
                capture_output=True,
                timeout=10,
                text=True
            )
            
            is_available = result.returncode == 0
            tool_config['status'] = 'available' if is_available else 'failed'
            
            if is_available:
                tool_config['last_success'] = datetime.now()
                tool_config['failures'] = 0
            else:
                tool_config['failures'] += 1
            
            return is_available
            
        except Exception as e:
            self.logger.error(f"❌ Error checking {tool_name}: {str(e)}")
            tool_config['status'] = 'error'
            tool_config['failures'] += 1
            return False
    
    def _auto_install_tool(self, tool_name: str) -> bool:
        """Attempt to automatically install a missing tool"""
        if tool_name not in self.tools:
            return False
        
        tool_config = self.tools[tool_name]
        self.logger.info(f"🔧 Attempting to install {tool_name}...")
        
        try:
            # Try to install using the configured command
            result = subprocess.run(
                tool_config['install_command'],
                capture_output=True,
                timeout=300,  # 5 minutes timeout
                text=True
            )
            
            if result.returncode == 0:
                self.logger.info(f"✅ Successfully installed {tool_name}")
                tool_config['status'] = 'installed'
                return self._check_tool_availability(tool_name)
            else:
                self.logger.error(f"❌ Failed to install {tool_name}: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Error installing {tool_name}: {str(e)}")
            return False
    
    def _ensure_tool_available(self, tool_name: str) -> bool:
        """Ensure a tool is available, attempting recovery if needed"""
        # First check if tool is available
        if self._check_tool_availability(tool_name):
            return True
        
        self.logger.warning(f"⚠️ Tool {tool_name} not available, attempting recovery...")
        
        # Try to install the tool
        if self._auto_install_tool(tool_name):
            return True
        
        # If installation fails, try alternative approaches
        self.logger.error(f"❌ Failed to recover {tool_name}")
        return False
    
    def _execute_with_retry(self, tool_name: str, command: List[str], max_retries: int = 3) -> subprocess.CompletedProcess:
        """Execute tool command with retry logic"""
        for attempt in range(max_retries + 1):
            try:
                # Ensure tool is available before execution
                if not self._ensure_tool_available(tool_name):
                    raise Exception(f"Tool {tool_name} is not available")
                
                # Execute the command
                result = subprocess.run(
                    command,
                    capture_output=True,
                    timeout=300,  # 5 minutes timeout
                    text=True
                )
                
                # Record success
                self.tools[tool_name]['last_success'] = datetime.now()
                self.tools[tool_name]['failures'] = 0
                self.tools[tool_name]['status'] = 'healthy'
                
                return result
                
            except subprocess.TimeoutExpired as e:
                self.logger.warning(f"⚠️ {tool_name} command timed out (attempt {attempt + 1})")
                if attempt == max_retries:
                    raise e
                time.sleep(2 ** attempt)  # Exponential backoff
                
            except Exception as e:
                self.tools[tool_name]['failures'] += 1
                self.logger.warning(f"⚠️ {tool_name} execution failed (attempt {attempt + 1}): {str(e)}")
                
                if attempt == max_retries:
                    self.tools[tool_name]['status'] = 'failed'
                    raise e
                
                # Wait before retry
                time.sleep(2 ** attempt)
        
        # This should never be reached
        raise Exception(f"All retry attempts exhausted for {tool_name}")
    
    def enhanced_nmap(self, targets: List[str], additional_args: Optional[List[str]] = None) -> str:
        """Enhanced Nmap execution with self-healing"""
        self.logger.info(f"🔍 Running enhanced Nmap scan on {targets}")
        
        command = ['nmap', '-sV', '-Pn'] + (additional_args or []) + targets
        
        try:
            result = self._execute_with_retry('nmap', command)
            
            if result.returncode == 0:
                output = result.stdout
                self.logger.info("✅ Nmap scan completed successfully")
                return output
            else:
                error_msg = f"Nmap scan failed: {result.stderr}"
                self.logger.error(f"❌ {error_msg}")
                return f"Error: {error_msg}"
                
        except Exception as e:
            error_msg = f"Nmap execution error: {str(e)}"
            self.logger.error(f"❌ {error_msg}")
            return f"Error: {error_msg}"
    
    def enhanced_sqlmap(self, target_url: str, additional_args: Optional[List[str]] = None) -> str:
        """Enhanced SQLMap execution with self-healing"""
        self.logger.info(f"🌐 Running enhanced SQLMap on {target_url}")
        
        command = ['sqlmap', '-u', target_url] + (additional_args or [])
        
        try:
            result = self._execute_with_retry('sqlmap', command)
            
            output = result.stdout if result.stdout else result.stderr
            
            if result.returncode == 0 or "nothing to inject for" in output.lower():
                self.logger.info("✅ SQLMap scan completed successfully")
                return output
            else:
                error_msg = f"SQLMap scan failed: {result.stderr}"
                self.logger.error(f"❌ {error_msg}")
                return f"Error: {error_msg}"
                
        except Exception as e:
            error_msg = f"SQLMap execution error: {str(e)}"
            self.logger.error(f"❌ {error_msg}")
            return f"Error: {error_msg}"
    
    def enhanced_nikto(self, target_url: str, additional_args: Optional[List[str]] = None) -> str:
        """Enhanced Nikto execution with self-healing"""
        self.logger.info(f"🔒 Running enhanced Nikto on {target_url}")
        
        command = ['nikto', '-h', target_url] + (additional_args or [])
        
        try:
            result = self._execute_with_retry('nikto', command)
            
            output = result.stdout if result.stdout else result.stderr
            self.logger.info("✅ Nikto scan completed successfully")
            return output
                
        except Exception as e:
            error_msg = f"Nikto execution error: {str(e)}"
            self.logger.error(f"❌ {error_msg}")
            return f"Error: {error_msg}"
    
    def enhanced_masscan(self, targets: List[str], ports: str, additional_args: Optional[List[str]] = None) -> str:
        """Enhanced Masscan execution with self-healing"""
        self.logger.info(f"⚡ Running enhanced Masscan on {targets} ports {ports}")
        
        command = ['masscan'] + targets + ['-p', ports] + (additional_args or [])
        
        try:
            result = self._execute_with_retry('masscan', command)
            
            output = result.stdout if result.stdout else result.stderr
            self.logger.info("✅ Masscan completed successfully")
            return output
                
        except Exception as e:
            error_msg = f"Masscan execution error: {str(e)}"
            self.logger.error(f"❌ {error_msg}")
            return f"Error: {error_msg}"
    
    def health_check_all_tools(self) -> Dict[str, Any]:
        """Perform health check on all security tools"""
        self.logger.info("🩺 Performing comprehensive tool health check")
        
        health_status = {
            'timestamp': datetime.now().isoformat(),
            'tools': {},
            'overall_health': 'healthy'
        }
        
        for tool_name in self.tools.keys():
            tool_healthy = self._check_tool_availability(tool_name)
            health_status['tools'][tool_name] = {
                'healthy': tool_healthy,
                'status': self.tools[tool_name]['status'],
                'last_success': self.tools[tool_name]['last_success'].isoformat() if self.tools[tool_name]['last_success'] else None,
                'failures': self.tools[tool_name]['failures']
            }
            
            if not tool_healthy:
                health_status['overall_health'] = 'degraded'
        
        # Check if any tool is healthy
        healthy_tools = [tool for tool, status in health_status['tools'].items() if status['healthy']]
        if not healthy_tools:
            health_status['overall_health'] = 'critical'
        
        return health_status
    
    def auto_repair_all_tools(self) -> bool:
        """Attempt to repair all failed tools"""
        self.logger.info("🔧 Starting auto-repair for all tools")
        
        health_status = self.health_check_all_tools()
        failed_tools = [tool for tool, status in health_status['tools'].items() if not status['healthy']]
        
        if not failed_tools:
            self.logger.info("✅ All tools are already healthy")
            return True
        
        repair_success = True
        for tool_name in failed_tools:
            self.logger.info(f"🔧 Attempting to repair {tool_name}")
            if not self._auto_install_tool(tool_name):
                repair_success = False
        
        if repair_success:
            self.logger.info("✅ All tool repairs completed successfully")
        else:
            self.logger.warning("⚠️ Some tool repairs failed")
        
        return repair_success
    
    def get_tool_status(self) -> Dict[str, Any]:
        """Get current status of all tools"""
        return {
            'tools': self.tools.copy(),
            'last_health_check': datetime.now().isoformat()
        }

# Global instance for easy access
enhanced_tool_wrapper = EnhancedToolWrapper()