import subprocess
def run_sqlmap(target, options=None):
    cmd = ["sqlmap", "-u", target]
    if options:
        cmd += options
    print(f"[sqlmap_tool] Running: {' '.join(cmd)}")
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        output_lines = []
        if proc.stdout is not None:
            for line in proc.stdout:
                print(f"[sqlmap_tool][{target}] {line.strip()}")
                output_lines.append(line)
        proc.wait(timeout=120)
        if proc.returncode == 0:
            return {"output": ''.join(output_lines)}
        else:
            return {"error": ''.join(output_lines)}
    except Exception as e:
        return {"error": str(e)}
