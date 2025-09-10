#!/usr/bin/env python3
"""
🚀 AI_CODE ETHICAL HACKER - COMPLETE VERSION
Full-featured autonomous penetration testing platform
"""

import os
import sys
from pathlib import Path

# Set API keys in environment
os.environ["GROQ_API_KEY"] = "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"
os.environ["GOOGLE_API_KEY"] = "AIzaSyCbIDV8wJ-3TL8BtI_HPdWVUSClBgoRszM"

# Add project root to path
sys.path.append(str(Path(__file__).parent))

# Import and run the working system
from simple_main import SimpleEthicalHacker

def main():
    """
    🎯 AI_CODE Ethical Hacker Platform
    
    Complete autonomous penetration testing system with:
    ✅ AI-powered analysis using Groq openai/gpt-oss-120b
    ✅ Google Gemini fallback for complex reasoning
    ✅ Full security tools integration (Nmap, SQLMap, Nikto)
    ✅ Ghost mode operations and stealth features
    ✅ Interactive menu system
    ✅ Custom task planning with AI
    """
    
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║  🚀 AI_CODE ETHICAL HACKER - Complete Autonomous Testing Platform          ║
║                                                                            ║
║  ✅ Multi-Agent AI System     ✅ Security Tools Integration                ║
║  ✅ Groq OpenAI GPT-OSS-120B  ✅ Google Gemini Pro                        ║
║  ✅ Autonomous Operations     ✅ Ghost Mode Stealth                        ║
║  ✅ Professional Reporting    ✅ Lab Safety Controls                       ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    try:
        hacker = SimpleEthicalHacker()
        hacker.run()
    except KeyboardInterrupt:
        print("\n🛑 Operation safely terminated by user")
    except Exception as e:
        print(f"\n❌ Critical error: {e}")
        print("📞 Contact support if this issue persists")

if __name__ == "__main__":
    main()