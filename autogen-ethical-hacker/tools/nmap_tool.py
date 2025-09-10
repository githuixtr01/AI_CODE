import subprocess

def run_nmap(targets):
    results = {}
    for target in targets:
        try:
            print(f"[nmap_tool] Running: nmap -sV -Pn {target}")
            proc = subprocess.Popen([
                "nmap", "-sV", "-Pn", target
            ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
            output_lines = []
            if proc.stdout is not None:
                for line in proc.stdout:
                    print(f"[nmap_tool][{target}] {line.strip()}")
                    output_lines.append(line)
            proc.wait(timeout=60)
            if proc.returncode == 0:
                results[target] = {"output": ''.join(output_lines)}
            else:
                results[target] = {"error": ''.join(output_lines)}
        except Exception as e:
            results[target] = {"error": str(e)}
    return results
