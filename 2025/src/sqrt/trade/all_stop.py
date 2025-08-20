import os
import psutil
import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def kill_julia_process(name):
    for proc in psutil.process_iter(['pid', 'name']):
        if name in proc.info['name']:
            try:
                psutil.Process(proc.info['pid']).kill()
                logger.info(f"Process {name} with PID {proc.info['pid']} has been killed.")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

def kill_other_python_processes():
    current_pid = os.getpid()
    process = subprocess.Popen(['ps', '-eo', 'pid,cmd'], stdout=subprocess.PIPE, text=True)
    stdout, _ = process.communicate()

    for line in stdout.splitlines():
        if 'python' in line and str(current_pid) not in line:
            pid = int(line.split()[0])
            os.kill(pid, 9)

kill_julia_process("julia")
kill_other_python_processes()