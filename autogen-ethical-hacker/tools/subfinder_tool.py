import subprocess
def run_subfinder(domain):
    cmd = ["subfinder", "-d", domain]
    print(f"[subfinder_tool] Running: {' '.join(cmd)}")
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        output_lines = []
        if proc.stdout is not None:
            for line in proc.stdout:
                print(f"[subfinder_tool][{domain}] {line.strip()}")
                output_lines.append(line)
        proc.wait(timeout=60)
        if proc.returncode == 0:
            return {"output": ''.join(output_lines)}
        else:
            return {"error": ''.join(output_lines)}
    except Exception as e:
        return {"error": str(e)}
