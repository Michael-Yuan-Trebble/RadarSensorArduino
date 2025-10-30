import serial 
import csv
import time
from datetime import datetime
import os
import subprocess
import sys
import signal

PORT = "COM3"
BAUD = 9600
folder = os.path.join(os.path.dirname(__file__),"data")

exePath = os.path.join(os.path.dirname(__file__),"analyzer.exe")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
os.makedirs(folder,exist_ok=True)

OUTPUTFILE = f'{folder}/distances_{timestamp}.csv'

stop_requested = False

def request_stop(signum, frame):
    global stop_requested
    stop_requested = True

signal.signal(signal.SIGBREAK, request_stop)
signal.signal(signal.SIGINT, request_stop)

try:
    ser = serial.Serial(PORT,BAUD,timeout=1)
    time.sleep(5)
    ser.reset_input_buffer()
except:
    raise RuntimeError

with open(OUTPUTFILE, 'w',newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['time(s)','timeDifference(ms)','distance(cm)','angle(degrees)'])
    print(f"Logging started -> {OUTPUTFILE}")
    try:
        while not stop_requested:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if not line or ',' not in line:
                continue
            data = line.split(',')
            writer.writerow(data)
            f.flush()
    except KeyboardInterrupt:
        stop_requested = True

ser.close()
print("\nLogging stopped.")
subprocess.run([exePath, OUTPUTFILE])
sys.exit(0)