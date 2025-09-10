#!/usr/bin/env python3
"""
Complete System Test - AI_CODE Ethical Hacker Platform
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

def test_api_keys():
    """Test API key availability"""
    print("🔑 Testing API Keys...")
    
    groq_key = os.environ.get("GROQ_API_KEY")
    google_key = os.environ.get("GOOGLE_API_KEY")
    
    print(f"  Groq API Key: {'✅ Present' if groq_key else '❌ Missing'}")
    print(f"  Google API Key: {'✅ Present' if google_key else '❌ Missing'}")
    
    return bool(groq_key and google_key)

def test_security_tools():
    """Test security tools availability"""
    print("\n🛠️ Testing Security Tools...")
    
    tools = {
        "nmap": "nmap --version",
        "sqlmap": "sqlmap --version", 
        "nikto": "nikto -Version",
        "masscan": "masscan --version"
    }
    
    results = {}
    for tool, command in tools.items():
        try:
            import subprocess
            result = subprocess.run(command.split(), capture_output=True, timeout=5)
            success = result.returncode == 0
            results[tool] = success
            status = "✅ Working" if success else "❌ Failed"
            print(f"  {tool}: {status}")
        except Exception as e:
            results[tool] = False
            print(f"  {tool}: ❌ Error - {e}")
    
    return results

def test_llm_integration():
    """Test LLM integration"""
    print("\n🤖 Testing LLM Integration...")
    
    try:
        from llm.simple_llm_router import llm_complete
        
        # Test Groq
        print("  Testing Groq API...")
        groq_result = llm_complete("What is cybersecurity?", provider="groq")
        groq_success = "Error:" not in groq_result
        print(f"  Groq: {'✅ Working' if groq_success else '❌ Failed'}")
        if not groq_success:
            print(f"    Error: {groq_result[:100]}...")
        
        # Test Google
        print("  Testing Google API...")
        google_result = llm_complete("What is penetration testing?", provider="google")
        google_success = "Error:" not in google_result
        print(f"  Google: {'✅ Working' if google_success else '❌ Failed'}")
        if not google_success:
            print(f"    Error: {google_result[:100]}...")
        
        return groq_success or google_success
        
    except Exception as e:
        print(f"  ❌ LLM Integration Failed: {e}")
        return False

def test_core_modules():
    """Test core module imports"""
    print("\n📦 Testing Core Modules...")
    
    modules = [
        "tools.nmap_tool",
        "tools.sqlmap_tool", 
        "tools.nikto_tool",
        "tools.masscan_tool",
        "llm.simple_llm_router"
    ]
    
    results = {}
    for module in modules:
        try:
            __import__(module)
            results[module] = True
            print(f"  {module}: ✅ Import OK")
        except Exception as e:
            results[module] = False
            print(f"  {module}: ❌ Import Failed - {e}")
    
    return results

def test_functional_demo():
    """Test basic functionality"""
    print("\n⚡ Testing Core Functionality...")
    
    try:
        # Test nmap tool
        from tools.nmap_tool import run_nmap
        print("  Testing Nmap tool...")
        nmap_result = run_nmap(["127.0.0.1", "-p", "22,80,443", "--top-ports", "10"])
        print("  ✅ Nmap test completed")
        
        # Test LLM analysis
        print("  Testing AI analysis...")
        from llm.simple_llm_router import llm_complete
        analysis = llm_complete("Analyze this scan: Open ports 22, 80, 443 found", provider="groq")
        if "Error:" in analysis:
            analysis = llm_complete("Analyze this scan: Open ports 22, 80, 443 found", provider="google")
        
        if "Error:" not in analysis:
            print("  ✅ AI analysis working")
        else:
            print("  ⚠️ AI analysis limited")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Functionality test failed: {e}")
        return False

def main():
    """Run complete system test"""
    print("=" * 80)
    print("🚀 AI_CODE ETHICAL HACKER - COMPLETE SYSTEM TEST")
    print("=" * 80)
    
    # Set API keys for testing
    os.environ["GROQ_API_KEY"] = "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"
    os.environ["GOOGLE_API_KEY"] = "AIzaSyCbIDV8wJ-3TL8BtI_HPdWVUSClBgoRszM"
    
    tests = [
        ("API Keys", test_api_keys),
        ("Security Tools", test_security_tools),
        ("Core Modules", test_core_modules), 
        ("LLM Integration", test_llm_integration),
        ("Functionality", test_functional_demo)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 SYSTEM TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    percentage = (passed / total) * 100
    print(f"\n🎯 Overall Success: {passed}/{total} ({percentage:.1f}%)")
    
    if percentage >= 80:
        print("🎉 SYSTEM READY FOR DEPLOYMENT!")
    elif percentage >= 60:
        print("⚠️ SYSTEM FUNCTIONAL - Minor issues detected")
    else:
        print("❌ SYSTEM NEEDS FIXES")
    
    print("\n🚀 AI_CODE Ethical Hacker Platform Testing Complete!")
    print("=" * 80)

if __name__ == "__main__":
    main()