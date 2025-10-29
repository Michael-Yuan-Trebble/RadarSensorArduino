import serial 
import csv
import time
from datetime import datetime
import os
import subprocess

PORT = "COM3"
BAUD = 9600
folder = "data"

exePath = os.path.join(os.path.dirname(__file__),"analyzer.exe")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
os.makedirs(folder,exist_ok=True)

OUTPUTFILE = f'{folder}/distances_{timestamp}.csv'

ser = serial.Serial(PORT,BAUD,timeout=1)
time.sleep(5)
ser.reset_input_buffer()

with open(OUTPUTFILE, 'w',newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['time(s)','timeDifference(ms)','distance(cm)','angle(degrees)'])
    print(f"Logging started -> {OUTPUTFILE}")
    try:
        while True:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if not line or ',' not in line:
                continue
            data = line.split(',')
            writer.writerow(data)
            f.flush()
    except KeyboardInterrupt:
        print("\nLogging stopped.")
        subprocess.run([exePath, OUTPUTFILE])