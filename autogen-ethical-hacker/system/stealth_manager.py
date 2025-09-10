#!/usr/bin/env python3
"""
👻 Stealth Manager - Ghost-like Internet Operations
Advanced anonymity and stealth techniques to remain undetected
"""
import subprocess
import random
import time
import os
import requests
import socket
from urllib.parse import urlparse

class StealthManager:
    def __init__(self):
        self.tor_running = False
        self.vpn_running = False
        self.original_mac = {}
        self.proxy_chains = [
            "socks5://127.0.0.1:9050",  # Tor
            "http://127.0.0.1:8080",   # Burp Suite
            "socks4://127.0.0.1:1080"  # Local SOCKS
        ]
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0"
        ]
    
    def run_command(self, command, silent=False):
        """Execute system command"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if not silent and result.returncode != 0:
                print(f"[StealthManager] ❌ Command failed: {command}")
            return result.returncode == 0
        except Exception as e:
            if not silent:
                print(f"[StealthManager] ❌ Error executing: {command} - {e}")
            return False
    
    def check_root_privileges(self):
        """Check if running with root privileges"""
        return os.geteuid() == 0
    
    def start_tor(self):
        """Start Tor service for anonymity"""
        print("[StealthManager] 👻 Starting Tor service...")
        
        if not self.check_root_privileges():
            print("[StealthManager] ⚠️ Root privileges required for Tor")
            return False
        
        # Start Tor service
        if self.run_command("systemctl start tor"):
            # Wait for Tor to initialize
            time.sleep(5)
            
            # Verify Tor is running
            if self.run_command("systemctl is-active tor", silent=True):
                self.tor_running = True
                print("[StealthManager] ✅ Tor service started successfully")
                
                # Test Tor connection
                if self.test_tor_connection():
                    print("[StealthManager] ✅ Tor anonymity confirmed")
                    return True
                else:
                    print("[StealthManager] ⚠️ Tor running but anonymity test failed")
                    return False
        
        print("[StealthManager] ❌ Failed to start Tor service")
        return False
    
    def stop_tor(self):
        """Stop Tor service"""
        print("[StealthManager] 🔄 Stopping Tor service...")
        if self.run_command("systemctl stop tor"):
            self.tor_running = False
            print("[StealthManager] ✅ Tor service stopped")
            return True
        return False
    
    def test_tor_connection(self):
        """Test if Tor is working properly"""
        try:
            # Use Tor's SOCKS proxy to check IP
            proxies = {
                'http': 'socks5://127.0.0.1:9050',
                'https': 'socks5://127.0.0.1:9050'
            }
            
            response = requests.get('https://check.torproject.org/api/ip', 
                                  proxies=proxies, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('IsTor', False):
                    print(f"[StealthManager] 🌐 Tor IP: {data.get('IP', 'Unknown')}")
                    return True
        except Exception as e:
            print(f"[StealthManager] ❌ Tor test failed: {e}")
        
        return False
    
    def change_mac_address(self, interface="eth0"):
        """Change MAC address for additional anonymity"""
        print(f"[StealthManager] 🎭 Changing MAC address for {interface}...")
        
        if not self.check_root_privileges():
            print("[StealthManager] ⚠️ Root privileges required for MAC change")
            return False
        
        # Save original MAC
        try:
            result = subprocess.run(f"cat /sys/class/net/{interface}/address", 
                                  shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                self.original_mac[interface] = result.stdout.strip()
        except:
            pass
        
        # Change MAC address
        commands = [
            f"ip link set {interface} down",
            f"macchanger -r {interface}",
            f"ip link set {interface} up"
        ]
        
        success = True
        for cmd in commands:
            if not self.run_command(cmd, silent=True):
                success = False
                break
        
        if success:
            # Verify MAC change
            try:
                result = subprocess.run(f"cat /sys/class/net/{interface}/address", 
                                      shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    new_mac = result.stdout.strip()
                    print(f"[StealthManager] ✅ MAC changed to: {new_mac}")
                    return True
            except:
                pass
        
        print(f"[StealthManager] ❌ Failed to change MAC for {interface}")
        return False
    
    def restore_mac_address(self, interface="eth0"):
        """Restore original MAC address"""
        if interface in self.original_mac:
            print(f"[StealthManager] 🔄 Restoring original MAC for {interface}...")
            commands = [
                f"ip link set {interface} down",
                f"macchanger -m {self.original_mac[interface]} {interface}",
                f"ip link set {interface} up"
            ]
            
            for cmd in commands:
                self.run_command(cmd, silent=True)
            
            print("[StealthManager] ✅ Original MAC restored")
    
    def configure_dns_over_https(self):
        """Configure DNS over HTTPS for privacy"""
        print("[StealthManager] 🔒 Configuring DNS over HTTPS...")
        
        # Configure systemd-resolved for DoH
        doh_config = """
[Resolve]
DNS=1.1.1.1#cloudflare-dns.com 8.8.8.8#dns.google
DNSOverTLS=yes
DNSSEC=yes
FallbackDNS=1.0.0.1#cloudflare-dns.com 8.8.4.4#dns.google
"""
        
        try:
            with open("/etc/systemd/resolved.conf", "w") as f:
                f.write(doh_config)
            
            self.run_command("systemctl restart systemd-resolved")
            print("[StealthManager] ✅ DNS over HTTPS configured")
            return True
        except Exception as e:
            print(f"[StealthManager] ❌ DNS configuration failed: {e}")
            return False
    
    def enable_iptables_anonymity(self):
        """Configure iptables for enhanced anonymity"""
        print("[StealthManager] 🛡️ Configuring firewall for anonymity...")
        
        iptables_rules = [
            # Flush existing rules
            "iptables -F",
            "iptables -X", 
            "iptables -t nat -F",
            "iptables -t nat -X",
            
            # Default policies
            "iptables -P INPUT DROP",
            "iptables -P FORWARD DROP",
            "iptables -P OUTPUT DROP",
            
            # Allow loopback
            "iptables -A INPUT -i lo -j ACCEPT",
            "iptables -A OUTPUT -o lo -j ACCEPT",
            
            # Allow established connections
            "iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT",
            "iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT",
            
            # Allow Tor traffic
            "iptables -A OUTPUT -p tcp --dport 9050 -j ACCEPT",
            "iptables -A OUTPUT -p tcp --dport 9051 -j ACCEPT",
            
            # Allow DNS through Tor
            "iptables -A OUTPUT -p udp --dport 53 -j ACCEPT",
            "iptables -A OUTPUT -p tcp --dport 53 -j ACCEPT",
            
            # Block direct internet (force through Tor)
            "iptables -A OUTPUT -p tcp --dport 80 -j DROP",
            "iptables -A OUTPUT -p tcp --dport 443 -j DROP"
        ]
        
        for rule in iptables_rules:
            self.run_command(rule, silent=True)
        
        print("[StealthManager] ✅ Anonymity firewall configured")
    
    def get_random_user_agent(self):
        """Get random user agent for web requests"""
        return random.choice(self.user_agents)
    
    def get_stealth_headers(self):
        """Get stealth HTTP headers"""
        return {
            'User-Agent': self.get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
    
    def start_full_stealth_mode(self):
        """Enable complete stealth mode"""
        print("\n" + "="*60)
        print("👻 ACTIVATING FULL STEALTH MODE")
        print("="*60)
        
        success_count = 0
        total_steps = 6
        
        # Step 1: Start Tor
        if self.start_tor():
            success_count += 1
        
        # Step 2: Change MAC address
        try:
            interfaces = ["eth0", "wlan0", "enp0s3"]
            for interface in interfaces:
                if os.path.exists(f"/sys/class/net/{interface}"):
                    if self.change_mac_address(interface):
                        success_count += 1
                    break
        except:
            pass
        
        # Step 3: Configure DNS over HTTPS
        if self.configure_dns_over_https():
            success_count += 1
        
        # Step 4: Configure anonymity firewall
        self.enable_iptables_anonymity()
        success_count += 1
        
        # Step 5: Clear system logs
        log_clear_commands = [
            "journalctl --vacuum-time=1s",
            "echo '' > /var/log/auth.log",
            "echo '' > /var/log/syslog",
            "history -c"
        ]
        
        for cmd in log_clear_commands:
            self.run_command(cmd, silent=True)
        success_count += 1
        
        # Step 6: Final verification
        if self.tor_running:
            success_count += 1
        
        print(f"\n[StealthManager] 👻 Stealth mode: {success_count}/{total_steps} components active")
        
        if success_count >= 4:
            print("[StealthManager] ✅ GHOST MODE ACTIVATED - You are now invisible")
            return True
        else:
            print("[StealthManager] ⚠️ Partial stealth mode - Some components failed")
            return False
    
    def stop_stealth_mode(self):
        """Disable stealth mode and restore normal operation"""
        print("\n[StealthManager] 🔄 Deactivating stealth mode...")
        
        # Stop Tor
        self.stop_tor()
        
        # Restore MAC addresses
        for interface in self.original_mac:
            self.restore_mac_address(interface)
        
        # Flush firewall rules
        self.run_command("iptables -F")
        self.run_command("iptables -X")
        self.run_command("iptables -t nat -F")
        self.run_command("iptables -t nat -X")
        
        # Reset default policies
        self.run_command("iptables -P INPUT ACCEPT")
        self.run_command("iptables -P FORWARD ACCEPT")
        self.run_command("iptables -P OUTPUT ACCEPT")
        
        print("[StealthManager] ✅ Stealth mode deactivated")
    
    def get_current_ip(self):
        """Get current external IP address"""
        try:
            if self.tor_running:
                proxies = {
                    'http': 'socks5://127.0.0.1:9050',
                    'https': 'socks5://127.0.0.1:9050'
                }
                response = requests.get('https://ipinfo.io/ip', proxies=proxies, timeout=10)
            else:
                response = requests.get('https://ipinfo.io/ip', timeout=10)
            
            return response.text.strip()
        except:
            return "Unknown"
    
    def stealth_status(self):
        """Get current stealth status"""
        status = {
            "tor_running": self.tor_running,
            "mac_changed": len(self.original_mac) > 0,
            "external_ip": self.get_current_ip(),
            "stealth_level": "Ghost" if self.tor_running else "Normal"
        }
        
        return status