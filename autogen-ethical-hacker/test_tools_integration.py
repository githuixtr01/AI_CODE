import subprocess
import json
import os

TOOLS_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config", "tools_config.json")

def check_tool(path):
    try:
        result = subprocess.run([path, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        if result.returncode == 0 or result.stdout or result.stderr:
            print(f"✅ {os.path.basename(path)} found and executable.")
            return True
        else:
            print(f"❌ {os.path.basename(path)} not working.")
            return False
    except Exception as e:
        print(f"❌ {os.path.basename(path)} error: {e}")
        return False

def main():
    with open(TOOLS_CONFIG_PATH, "r") as f:
        tools = json.load(f)
    print("\nTool Integration Test Results:")
    for tool, path in tools.items():
        check_tool(path)

if __name__ == "__main__":
    main()
