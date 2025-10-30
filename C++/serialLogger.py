import serial, csv, time
import os, sys, subprocess
from datetime import datetime

PORT = "COM3"
BAUD = 9600
folder = os.path.join(os.path.dirname(__file__), "data")
exePath = os.path.join(os.path.dirname(__file__), "analyzer.exe")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
os.makedirs(folder, exist_ok=True)
OUTPUTFILE = f'{folder}/distances_{timestamp}.csv'

stop_requested = False

try:
    ser = serial.Serial(PORT, BAUD, timeout=1)
    time.sleep(3)
    ser.reset_input_buffer()
except:
    sys.stdout.write("SERIAL_FAIL\n")
    sys.stdout.flush()
    sys.exit(0)

stopFile = os.path.join(os.path.dirname(__file__), "stop.flag")

with open(OUTPUTFILE, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['time(s)', 'timeDifference(ms)', 'distance(cm)', 'angle(degrees)'])

    sys.stdout.write("INIT_OK\n")
    sys.stdout.flush()

    while not os.path.exists(stopFile):
        line = ser.readline()
        if line:
            line = line.decode(errors='ignore').strip()
            if ',' in line:
                writer.writerow(line.split(','))
                f.flush()
            time.sleep(0.01)

ser.close()
sys.stdout.write("LOGGING_STOPPED\n")
sys.stdout.flush()
subprocess.run([exePath, OUTPUTFILE])

sys.exit(0)