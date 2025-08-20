import psutil


def kill_process(name):
    for proc in psutil.process_iter(["pid", "name"]):
        if name in proc.info["name"]:
            try:
                psutil.Process(proc.info["pid"]).kill()
                print(f"Process {name} with PID {proc.info['pid']} has been killed.")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass


kill_process("python")
kill_process("julia")
