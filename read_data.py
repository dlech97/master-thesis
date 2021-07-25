import serial
import time
from datetime import datetime
from matplotlib import pyplot as plt
import collections
import logging

DWM = serial.Serial(port='COM5', baudrate=115200)
DWM.write("reset\r".encode())
time.sleep(1)
DWM.write('\r\r'.encode())
time.sleep(1)
DWM.write('lec\r'.encode())

logging.basicConfig(filename="log.txt", filemode="w", level=logging.INFO)
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
logging.getLogger("").addHandler(console)

fig = plt.figure()
plt.axis([0, 3, 0, 6])

p_cnt = 0

# ShReg = collections.deque((), 3)

while True:
    try:
        line = DWM.readline()
        p_cnt += 1
        if p_cnt % 3:
            continue
        if line:
            parse = line.decode("utf-8").split(",")
            print(parse)
            module_id = parse[2]
            x = float(parse[3])
            y = float(parse[4])
            z = float(parse[5])
            quality = parse[6]
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            logging.info("Datetime: {:} | position: {:2.2f} {:2.2f} {:2.2f}".format(dt_string, x, y, z))
            # ShReg.append((x, y))
            plt.axis([0, 3, 0, 6])
            # for (x, y) in ShReg:
            plt.scatter(x, y)
            plt.pause(0.001)
            plt.clf()
    except Exception as e:
        print(e)
        continue
