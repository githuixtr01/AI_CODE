#!/usr/bin/env python3
"""
🔧 Kali Linux Auto-Installer for Ethical Hacking Tools
Automatically installs and configures all required penetration testing tools
"""
import subprocess
import sys
import os
import time
from pathlib import Path

class KaliAutoInstaller:
    def __init__(self):
        self.required_tools = {
            # Network scanning and enumeration
            "nmap": "apt-get install -y nmap",
            "masscan": "apt-get install -y masscan", 
            "rustscan": "wget -qO- https://github.com/RustScan/RustScan/releases/download/2.0.1/rustscan_2.0.1_amd64.deb && dpkg -i rustscan_2.0.1_amd64.deb",
            "nuclei": "GO111MODULE=on go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest",
            
            # Web application testing
            "gobuster": "apt-get install -y gobuster",
            "dirb": "apt-get install -y dirb",
            "dirbuster": "apt-get install -y dirbuster",
            "sqlmap": "apt-get install -y sqlmap",
            "wpscan": "apt-get install -y wpscan",
            "nikto": "apt-get install -y nikto",
            "burpsuite": "apt-get install -y burpsuite",
            
            # Exploitation frameworks
            "metasploit-framework": "apt-get install -y metasploit-framework",
            "msfvenom": "apt-get install -y metasploit-framework",
            "searchsploit": "apt-get install -y exploitdb",
            
            # Password attacks
            "hydra": "apt-get install -y hydra",
            "john": "apt-get install -y john",
            "hashcat": "apt-get install -y hashcat",
            "crunch": "apt-get install -y crunch",
            
            # Network analysis
            "wireshark": "apt-get install -y wireshark",
            "tcpdump": "apt-get install -y tcpdump",
            "netcat": "apt-get install -y netcat-traditional",
            
            # Steganography and forensics
            "steghide": "apt-get install -y steghide",
            "binwalk": "apt-get install -y binwalk",
            "exiftool": "apt-get install -y exiftool",
            
            # Anonymity and stealth tools
            "tor": "apt-get install -y tor",
            "proxychains": "apt-get install -y proxychains",
            "macchanger": "apt-get install -y macchanger",
            "anonsurf": "git clone https://github.com/Und3rf10w/kali-anonsurf.git && cd kali-anonsurf && ./installer.sh",
            
            # Additional tools
            "docker.io": "apt-get install -y docker.io",
            "python3-pip": "apt-get install -y python3-pip",
            "git": "apt-get install -y git",
            "curl": "apt-get install -y curl",
            "wget": "apt-get install -y wget"
        }
        
        self.python_packages = [
            "requests", "beautifulsoup4", "lxml", "selenium", 
            "scapy", "python-nmap", "paramiko", "pycryptodome",
            "colorama", "termcolor", "tqdm", "psutil"
        ]
        
        self.go_tools = {
            "subfinder": "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
            "assetfinder": "github.com/tomnomnom/assetfinder@latest",
            "httprobe": "github.com/tomnomnom/httprobe@latest",
            "waybackurls": "github.com/tomnomnom/waybackurls@latest"
        }

    def run_command(self, command, timeout=300):
        """Execute system command with timeout"""
        try:
            print(f"[AutoInstaller] 🔧 Executing: {command}")
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=timeout
            )
            if result.returncode == 0:
                print(f"[AutoInstaller] ✅ Success: {command}")
                return True
            else:
                print(f"[AutoInstaller] ❌ Failed: {command} - {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print(f"[AutoInstaller] ⏰ Timeout: {command}")
            return False
        except Exception as e:
            print(f"[AutoInstaller] ❌ Error: {command} - {e}")
            return False

    def check_root(self):
        """Check if running as root"""
        if os.geteuid() != 0:
            print("[AutoInstaller] ❌ Root privileges required for installation")
            print("[AutoInstaller] 🔧 Please run with sudo")
            return False
        return True

    def update_system(self):
        """Update package repositories"""
        print("[AutoInstaller] 🔄 Updating system packages...")
        commands = [
            "apt-get update",
            "apt-get upgrade -y",
            "apt-get install -y software-properties-common apt-transport-https"
        ]
        
        for cmd in commands:
            self.run_command(cmd)

    def install_go(self):
        """Install Go programming language"""
        if self.run_command("which go"):
            print("[AutoInstaller] ✅ Go already installed")
            return True
            
        print("[AutoInstaller] 🔧 Installing Go...")
        commands = [
            "wget -q https://golang.org/dl/go1.21.0.linux-amd64.tar.gz",
            "tar -C /usr/local -xzf go1.21.0.linux-amd64.tar.gz",
            "echo 'export PATH=$PATH:/usr/local/go/bin' >> /etc/profile",
            "export PATH=$PATH:/usr/local/go/bin"
        ]
        
        for cmd in commands:
            self.run_command(cmd)

    def install_kali_tools(self):
        """Install all required Kali Linux tools"""
        print("[AutoInstaller] 🔧 Installing Kali Linux penetration testing tools...")
        
        failed_tools = []
        
        for tool, install_cmd in self.required_tools.items():
            print(f"[AutoInstaller] 📦 Installing {tool}...")
            
            # Check if tool already exists
            if self.run_command(f"which {tool}") or self.run_command(f"dpkg -l | grep {tool}"):
                print(f"[AutoInstaller] ✅ {tool} already installed")
                continue
            
            # Install the tool
            if not self.run_command(install_cmd):
                failed_tools.append(tool)
        
        if failed_tools:
            print(f"[AutoInstaller] ⚠️ Failed to install: {failed_tools}")
        else:
            print("[AutoInstaller] ✅ All Kali tools installed successfully")

    def install_python_packages(self):
        """Install required Python packages"""
        print("[AutoInstaller] 🐍 Installing Python packages...")
        
        for package in self.python_packages:
            self.run_command(f"pip3 install {package}")

    def install_go_tools(self):
        """Install Go-based security tools"""
        print("[AutoInstaller] 🔧 Installing Go security tools...")
        
        for tool, package in self.go_tools.items():
            print(f"[AutoInstaller] 📦 Installing {tool}...")
            self.run_command(f"go install -v {package}")

    def configure_stealth_tools(self):
        """Configure stealth and anonymity tools"""
        print("[AutoInstaller] 👻 Configuring stealth tools...")
        
        # Configure Tor
        tor_config = """
SocksPort 9050
ControlPort 9051
CookieAuthentication 1
DataDirectory /var/lib/tor
ExitNodes {us},{uk},{de},{fr},{ca}
StrictNodes 1
"""
        
        with open("/etc/tor/torrc", "w") as f:
            f.write(tor_config)
        
        # Configure ProxyChains
        proxychains_config = """
strict_chain
proxy_dns
tcp_read_time_out 15000
tcp_connect_time_out 8000

[ProxyList]
socks5 127.0.0.1 9050
"""
        
        with open("/etc/proxychains.conf", "w") as f:
            f.write(proxychains_config)
        
        # Start Tor service
        self.run_command("systemctl enable tor")
        self.run_command("systemctl start tor")
        
        print("[AutoInstaller] 👻 Stealth configuration completed")

    def create_aliases(self):
        """Create useful aliases for penetration testing"""
        aliases = """
# Penetration Testing Aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'
alias grep='grep --color=auto'

# Networking aliases
alias ports='netstat -tulanp'
alias myip='curl -s ifconfig.me'
alias listen='netstat -pnltu'

# Stealth aliases
alias anon='service tor start && export ALL_PROXY=socks5://127.0.0.1:9050'
alias unanon='service tor stop && unset ALL_PROXY'
alias newmac='macchanger -r'

# Security aliases
alias nmap-quick='nmap -T4 -F'
alias nmap-intense='nmap -T4 -A -v'
alias web-enum='gobuster dir -u'
alias sql-test='sqlmap -u'
"""
        
        with open("/root/.bashrc", "a") as f:
            f.write(aliases)
        
        print("[AutoInstaller] ✅ Penetration testing aliases created")

    def install_all(self):
        """Master installation function"""
        print("🚀 AutoGen Ethical Hacker - Kali Linux Auto-Installer")
        print("=" * 60)
        
        if not self.check_root():
            return False
        
        try:
            self.update_system()
            self.install_go()
            self.install_kali_tools()
            self.install_python_packages()
            self.install_go_tools()
            self.configure_stealth_tools()
            self.create_aliases()
            
            print("\n🎉 Installation completed successfully!")
            print("🔄 Please restart your terminal or run 'source ~/.bashrc'")
            print("👻 Stealth mode configured - use 'anon' to enable anonymity")
            return True
            
        except Exception as e:
            print(f"❌ Installation failed: {e}")
            return False

def main():
    installer = KaliAutoInstaller()
    installer.install_all()

if __name__ == "__main__":
    main()