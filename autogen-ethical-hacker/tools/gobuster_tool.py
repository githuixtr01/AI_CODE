import subprocess
def run_gobuster(target, wordlist, mode="dir", extensions=None):
    cmd = ["gobuster", mode, "-u", target, "-w", wordlist]
    if extensions:
        cmd += ["-x", extensions]
    print(f"[gobuster_tool] Running: {' '.join(cmd)}")
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        output_lines = []
        if proc.stdout is not None:
            for line in proc.stdout:
                print(f"[gobuster_tool][{target}] {line.strip()}")
                output_lines.append(line)
        proc.wait(timeout=60)
        if proc.returncode == 0:
            return {"output": ''.join(output_lines)}
        else:
            return {"error": ''.join(output_lines)}
    except Exception as e:
        return {"error": str(e)}
