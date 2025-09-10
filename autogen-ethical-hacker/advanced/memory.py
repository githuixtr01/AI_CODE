"""
Persistent Memory / Knowledge Base
Implements a simple persistent store using a local JSON file.
"""

import json
import os

MEMORY_FILE = os.path.abspath("agent_memory.json")

def store_memory(data):
    """Store data (dict) in persistent memory file."""
    print(f"[memory] Storing data: {data}")
    try:
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "r") as f:
                memory = json.load(f)
        else:
            memory = []
        memory.append(data)
        with open(MEMORY_FILE, "w") as f:
            json.dump(memory, f, indent=2)
        print(f"[memory] Data stored in {MEMORY_FILE}")
        return True
    except Exception as e:
        print(f"[memory] Error storing data: {e}")
        return False

def query_memory(query):
    """Query memory for entries containing the query string."""
    print(f"[memory] Query: {query}")
    try:
        if not os.path.exists(MEMORY_FILE):
            print("[memory] No memory file found.")
            return []
        with open(MEMORY_FILE, "r") as f:
            memory = json.load(f)
        results = [entry for entry in memory if query.lower() in str(entry).lower()]
        print(f"[memory] Found {len(results)} matching entries.")
        return results
    except Exception as e:
        print(f"[memory] Error querying memory: {e}")
        return []
