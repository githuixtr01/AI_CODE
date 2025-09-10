import subprocess

def run_masscan(targets, ports="1-1000"):  # Example port range
    if isinstance(targets, str):
        targets = [targets]
    results = {}
    for target in targets:
        try:
            print(f"[masscan_tool] Running: masscan -p{ports} {target}")
            proc = subprocess.Popen([
                "masscan", "-p", ports, target
            ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
            output_lines = []
            if proc.stdout is not None:
                for line in proc.stdout:
                    print(f"[masscan_tool][{target}] {line.strip()}")
                    output_lines.append(line)
            proc.wait(timeout=60)
            if proc.returncode == 0:
                results[target] = {"output": ''.join(output_lines)}
            else:
                results[target] = {"error": ''.join(output_lines)}
        except Exception as e:
            results[target] = {"error": str(e)}
    return results
