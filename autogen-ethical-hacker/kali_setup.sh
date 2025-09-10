#!/bin/bash
#
# 🚀 AutoGen Ethical Hacker - Kali Linux Auto-Setup Script
# Complete autonomous setup for Kali Linux penetration testing environment
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Banner
echo -e "${PURPLE}"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                  🚀 AutoGen Ethical Hacker                    ║"
echo "║                    Kali Linux Auto-Setup                      ║"
echo "║              Complete Autonomous Installation                  ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}❌ This script must be run as root${NC}"
   echo -e "${YELLOW}🔧 Please run: sudo bash kali_setup.sh${NC}"
   exit 1
fi

echo -e "${BLUE}🔍 Checking system requirements...${NC}"

# Check if Kali Linux
if ! grep -q "kali" /etc/os-release 2>/dev/null; then
    echo -e "${YELLOW}⚠️ Not running on Kali Linux, continuing anyway...${NC}"
fi

# Update system
echo -e "${BLUE}🔄 Updating system packages...${NC}"
apt-get update -qq
apt-get upgrade -y -qq

# Install Python dependencies
echo -e "${BLUE}🐍 Installing Python dependencies...${NC}"
apt-get install -y python3 python3-pip python3-venv python3-dev
pip3 install --upgrade pip

# Install core penetration testing tools
echo -e "${BLUE}📦 Installing core penetration testing tools...${NC}"
apt-get install -y \
    nmap masscan  \
    gobuster dirb dirbuster sqlmap wpscan nikto burpsuite \
    metasploit-framework exploitdb \
    hydra john hashcat crunch \
    wireshark tcpdump netcat-traditional \
    steghide binwalk exiftool \
    tor proxychains macchanger \
    docker.io git curl wget

# Install Go for additional tools
echo -e "${BLUE}🔧 Installing Go programming language...${NC}"
if ! command -v go &> /dev/null; then
    wget -q https://golang.org/dl/go1.21.0.linux-amd64.tar.gz
    tar -C /usr/local -xzf go1.21.0.linux-amd64.tar.gz
    echo 'export PATH=$PATH:/usr/local/go/bin' >> /etc/profile
    echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
    export PATH=$PATH:/usr/local/go/bin
    rm go1.21.0.linux-amd64.tar.gz
fi

# Install Go-based security tools
echo -e "${BLUE}🛠️ Installing Go security tools...${NC}"
export PATH=$PATH:/usr/local/go/bin
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/tomnomnom/assetfinder@latest
go install -v github.com/tomnomnom/httprobe@latest
go install -v github.com/tomnomnom/waybackurls@latest

# Copy Go binaries to system path
if [ -d "/root/go/bin" ]; then
    cp /root/go/bin/* /usr/local/bin/ 2>/dev/null || true
fi

# Install Python packages for AutoGen
echo -e "${BLUE}🤖 Installing AutoGen and AI dependencies...${NC}"
pip3 install \
    autogen-agentchat \
    groq \
    google-generativeai \
    openai \
    requests \
    beautifulsoup4 \
    lxml \
    selenium \
    scapy \
    python-nmap \
    paramiko \
    pycryptodome \
    colorama \
    termcolor \
    tqdm \
    psutil \
    pyyaml \
    fastapi \
    uvicorn \
    streamlit \
    matplotlib \
    networkx \
    redis \
    docker

# Configure Tor for anonymity
echo -e "${BLUE}👻 Configuring anonymity tools...${NC}"
cat > /etc/tor/torrc << EOF
SocksPort 9050
ControlPort 9051
CookieAuthentication 1
DataDirectory /var/lib/tor
ExitNodes {us},{uk},{de},{fr},{ca}
StrictNodes 1
EOF

# Configure ProxyChains
cat > /etc/proxychains.conf << EOF
strict_chain
proxy_dns
tcp_read_time_out 15000
tcp_connect_time_out 8000

[ProxyList]
socks5 127.0.0.1 9050
EOF

# Enable and start services
echo -e "${BLUE}🚀 Starting services...${NC}"
systemctl enable tor
systemctl start tor
systemctl enable docker
systemctl start docker

# Create useful aliases
echo -e "${BLUE}⚡ Creating penetration testing aliases...${NC}"
cat >> ~/.bashrc << 'EOF'

# AutoGen Ethical Hacker Aliases
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
alias anon='service tor start && export ALL_PROXY=socks5://127.0.0.1:9050 && echo "👻 Anonymous mode activated"'
alias unanon='service tor stop && unset ALL_PROXY && echo "🔄 Normal mode restored"'
alias newmac='macchanger -r'
alias ghost='python3 autonomous_main.py --ghost'

# Security aliases
alias nmap-quick='nmap -T4 -F'
alias nmap-intense='nmap -T4 -A -v'
alias web-enum='gobuster dir -u'
alias sql-test='sqlmap -u'

# AutoGen aliases
alias autopentester='python3 autonomous_main.py --auto'
alias hackermenu='python3 main.py'
alias setup-apis='python3 autonomous_main.py --setup'
alias system-status='python3 autonomous_main.py --status'
EOF

# Make AutoGen executable
chmod +x autonomous_main.py
chmod +x main.py

# Create desktop shortcut
echo -e "${BLUE}🖥️ Creating desktop shortcuts...${NC}"
mkdir -p /root/Desktop

cat > /root/Desktop/AutoGen-Ethical-Hacker.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=AutoGen Ethical Hacker
Comment=AI-Powered Autonomous Penetration Testing
Exec=gnome-terminal -- bash -c 'cd $(pwd) && python3 main.py; bash'
Icon=applications-security
Terminal=true
Categories=Security;Network;
EOF

cat > /root/Desktop/AutoGen-Autonomous.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=AutoGen Autonomous Mode
Comment=Fully Autonomous Ethical Hacking
Exec=gnome-terminal -- bash -c 'cd $(pwd) && python3 autonomous_main.py --auto; bash'
Icon=applications-security
Terminal=true
Categories=Security;Network;
EOF

chmod +x /root/Desktop/*.desktop

# Create configuration directory
mkdir -p config

# Create initial API configuration if it doesn't exist
if [ ! -f "config/apis.json" ]; then
    cat > config/apis.json << EOF
{
  "groq": {
    "api_keys": [],
  "model": "openai/gpt-oss-120b",
    "primary": true
  },
  "google": {
    "api_keys": [],
    "model": "gemini-pro",
    "backup": true
  }
}
EOF
fi

# Create lab scope configuration
cat > config/lab_scope.json << EOF
{
  "allowed_targets": [
    "192.168.1.0/24",
    "192.168.56.0/24",
    "10.0.0.0/24",
    "172.16.0.0/24"
  ],
  "forbidden_targets": [
    "8.8.8.8",
    "1.1.1.1",
    "google.com",
    "github.com"
  ],
  "max_threads": 10,
  "timeout": 300
}
EOF

# Final setup
echo -e "${BLUE}🔧 Finalizing setup...${NC}"
updatedb  # Update locate database
ldconfig  # Update library cache

# Success message
echo -e "${GREEN}"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                    ✅ SETUP COMPLETED!                         ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${GREEN}🎉 AutoGen Ethical Hacker installation completed successfully!${NC}"
echo ""
echo -e "${YELLOW}📋 Quick Start Guide:${NC}"
echo -e "${BLUE}1. Setup API keys:${NC} python3 autonomous_main.py --setup"
echo -e "${BLUE}2. Interactive mode:${NC} python3 main.py"
echo -e "${BLUE}3. Autonomous mode:${NC} python3 autonomous_main.py --auto"
echo -e "${BLUE}4. Ghost mode:${NC} python3 autonomous_main.py --ghost"
echo -e "${BLUE}5. System status:${NC} python3 autonomous_main.py --status"
echo ""
echo -e "${YELLOW}👻 Stealth Commands:${NC}"
echo -e "${BLUE}• Enable anonymity:${NC} anon"
echo -e "${BLUE}• Disable anonymity:${NC} unanon"
echo -e "${BLUE}• Change MAC address:${NC} newmac eth0"
echo ""
echo -e "${PURPLE}🔑 Don't forget to add your API keys before first use!${NC}"
echo -e "${GREEN}🚀 Ready for autonomous ethical hacking operations!${NC}"

# Restart bash to load new aliases
echo -e "${YELLOW}🔄 Please restart your terminal or run 'source ~/.bashrc' to load new commands${NC}"
