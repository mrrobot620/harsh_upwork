import subprocess
import time

def check_connection(retries=5, delay=1):
    for _ in range(retries):
        result = subprocess.run(['adb', 'shell', 'ping', '-c', '1', 'google.com'], capture_output=True, text=True)
        output = result.stdout.strip()
        if "1 packets transmitted, 1 received" in output or "bytes from" in output:
            return True 
        time.sleep(delay) 
    return False 

check_connection()