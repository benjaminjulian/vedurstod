import time
import os, sys
import serial
import io
from datetime import datetime

data_path_t = "data/temp.csv"
data_path_h = "data/hum.csv"
data_path_c = "data/co2.csv"
data_path_b = "data/bar.csv"

if not os.path.isfile(data_path_t):
	f = open(data_path_t, "w")
	f.write("time,temp\n")
	f.close()

if not os.path.isfile(data_path_h):
	f = open(data_path_h, "w")
	f.write("time,hum\n")
	f.close()

if not os.path.isfile(data_path_c):
	f = open(data_path_c, "w")
	f.write("time,eco2\n")
	f.close()

if not os.path.isfile(data_path_b):
	f = open(data_path_b, "w")
	f.write("time,bar\n")
	f.close()

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=5)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
sio.flush()


while True:
	now = datetime.now()
	line = sio.readline().replace("\n", "")

	try:
		if ":" in line:
			cmd, val = line.split(":")
			
			if cmd == "hiti":
				f = open(data_path_t, "a")
				f.write(now.strftime("%Y-%m-%dT%H:%M:%SZ,"))
				f.write(val)
				f.write("\n")
				f.close()
				print(str(now) + ", hiti: " + val + '°C')
			elif cmd == "raki":
				f = open(data_path_h, "a")
				f.write(now.strftime("%Y-%m-%dT%H:%M:%SZ,"))
				f.write(val)
				f.write("\n")
				f.close()
				print(str(now) + ", raki: " + val + '%')
			elif cmd == "eco2":
				f = open(data_path_c, "a")
				f.write(now.strftime("%Y-%m-%dT%H:%M:%SZ,"))
				f.write(val)
				f.write("\n")
				f.close()
				print(str(now) + ", eCO2: " + val + 'ppm')
			elif cmd == "hpa":
				f = open(data_path_b, "a")
				f.write(now.strftime("%Y-%m-%dT%H:%M:%SZ,"))
				f.write(val)
				f.write("\n")
				f.close()
				print(str(now) + ", loft: " + val + 'hPa')
	except Exception as e:
		print(str(now) + ", villa: " + str(e))

	time.sleep(1)