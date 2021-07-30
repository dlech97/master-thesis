import serial
import time
from matplotlib import pyplot as plt
import collections
import logging
from pynput import keyboard

formatter = logging.Formatter('%(asctime)s %(message)s')

PLOTTING = False
log_filename = "running_7.txt"


def setup_logger(file_name):
    handler = logging.FileHandler(file_name)
    handler.setFormatter(formatter)
    logger = logging.getLogger('logger')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger


def on_press(key):
    try:
        global logger
        if key.char == 's':
            print("Stopping")
            logger.info("STOP *")
        if key.char == "r":
            logger.info("RESUME *")
    except AttributeError:
        print('special key {} pressed'.format(key.char))


def on_release(key):
    if key == keyboard.Key.esc:
        return False


listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

logger = setup_logger(log_filename)
logger.info("STOP *")

DWM = serial.Serial(port='COM5', baudrate=115200)
DWM.write("reset\r".encode())
time.sleep(1)
DWM.write('\r\r'.encode())
time.sleep(1)
DWM.write('lec\r'.encode())

if PLOTTING:
    axis = [-5, 15, -5, 15]
    fig = plt.figure()
    plt.axis(axis)
    ShReg = collections.deque((), 3)

p_cnt = 0

while True:
    try:
        line = DWM.readline()
        if PLOTTING:
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
            quality = float(parse[6])
            logger.info("position: {:2.2f} {:2.2f} {:2.2f} quality: {:2.2f}".format(x, y, z, quality))
            if PLOTTING:
                # ShReg.append((x, y))
                plt.axis(axis)
                # for (x, y) in ShReg:
                plt.scatter(x, y)
                plt.pause(0.001)
                plt.clf()
    except Exception as e:
        print(e)
        continue
