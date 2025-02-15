import subprocess
import re
import sys
import os
import time

class ADB:
    def __init__(self):
        print(f"Starting ADB Handler for Script")
        if not self.check_device():
            print('No devices found existing')
            sys.exit()
        os.system('adb shell svc data enable')

    def check_device(self) -> bool:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        output = result.stdout.strip()
        pattern = re.compile(r"^(\S+)\s+device$", re.MULTILINE)
        matches = pattern.findall(output)

        if matches:
            print("Found Devices:", matches)
            return True
        elif len(matches) > 1:
            print(f"Existing multiple Devices Found: ", [matches])
            sys.exit()
        else:
            return False
        
    def toggle_internet(self):
        os.system("adb shell svc data disable")
        print('Turning off internet to change IP')
        time.sleep(.5)
        os.system('adb shell svc data enable')
        print(f'Internet IP Changed Successfully')
        time.sleep(1)


