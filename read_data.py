import socket
from struct import unpack
import time
from datetime import datetime
import numpy as np
from matplotlib import pyplot as plt
from sympy import symbols, solve_poly_system, re, im
import collections
import logging

# Configure UDP transmission
sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host, port = '0.0.0.0', 65000
server_address = (host, port)
sckt.bind(server_address)
print("Started listening...")

logging.basicConfig(filename="log.txt", filemode="w", level=logging.INFO)
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
logging.getLogger("").addHandler(console)

# # Receive location of anchors
# message, ad = sckt.recvfrom(4096)
# x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4 = unpack('12f', message)

# Prepare plot and variables for symbolic calculation
position_counter = 0
fig = plt.figure()
plt.axis([0, 3, 0, 6])
# x, y, z, w = symbols('x y z w')

# Position = collections.namedtuple('Position', ['x', 'y'])
ShReg = collections.deque((), 5)

message, addr = sckt.recvfrom(4096)
x, y, z = unpack('3f', message)
ShReg.append((x, y))

while True:
    # if position_counter % 2:
    #     continue
    # Receive distances from tag to all of anchors
    message, addr = sckt.recvfrom(4096)
    x, y, z = unpack('3f', message)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    logging.info("Datetime: {:} | position: {:2.2f} {:2.2f} {:2.2f}".format(dt_string, x, y, z))
    ShReg.append((x, y))
    print(ShReg)
    # print("distances: {:2.2f} {:2.2f} {:2.2f} {:2.2f}".format(d1, d2, d3, d4))
    # Solve for position symbolically
    # set_of_equations1234 = [np.square(x1 - x) + np.square(y1 - y) + np.square(z1 - z) - np.square(d1) + w,
    #                     np.square(x2 - x) + np.square(y2 - y) + np.square(z2 - z) - np.square(d2) + w,
    #                     np.square(x3 - x) + np.square(y3 - y) + np.square(z3 - z) - np.square(d3) + w,
    #                     np.square(x4 - x) + np.square(y4 - y) + np.square(z4 - z) - np.square(d4) + w]
    #
    # set_of_equations124 = [np.square(x1 - x) + np.square(y1 - y) + np.square(z1 - z) - np.square(d1),
    #                     np.square(x2 - x) + np.square(y2 - y) + np.square(z2 - z) - np.square(d2),
    #                     np.square(x4 - x) + np.square(y4 - y) + np.square(z4 - z) - np.square(d4)]
    #
    # set_of_equations134 = [np.square(x1 - x) + np.square(y1 - y) + np.square(z1 - z) - np.square(d1),
    #                     np.square(x4 - x) + np.square(y4 - y) + np.square(z4 - z) - np.square(d4),
    #                     np.square(x3 - x) + np.square(y3 - y) + np.square(z3 - z) - np.square(d3)]
    #
    # set_of_equations234 = [np.square(x4 - x) + np.square(y4 - y) + np.square(z4 - z) - np.square(d4),
    #                     np.square(x2 - x) + np.square(y2 - y) + np.square(z2 - z) - np.square(d2),
    #                     np.square(x3 - x) + np.square(y3 - y) + np.square(z3 - z) - np.square(d3)]
    # s123 = solve_poly_system(set_of_equations1234, x, y, z)[0]
    # z_pos = re(s123[2]) + im(s123[2])
    # x_pos = s123[0]
    # y_pos = s123[1]
    print("x:{:2.2f} y:{:2.2f} z:{:2.2f}".format(x, y, z))
    plt.axis([0, 3, 0, 6])
    for (x, y) in ShReg:
        plt.scatter(x, y)
    plt.pause(0.001)
    plt.clf()
    # try:
    #     s124 = solve_poly_system(set_of_equations124, x, y, z)[0]
    #     z_pos = re(s124[2]) + im(s124[2])
    #     x_pos = s124[0]
    #     y_pos = s124[1]
    #     print("x:{:2.2f} y:{:2.2f} z:{:2.2f}".format(x_pos, y_pos, z_pos))
    #     plt.scatter(x_pos, y_pos)
    #     plt.pause(0.01)
    # except NameError:
    #     print("Failed to solve eq. 2")
    # except NotImplementedError:
    #     print("Failed to solve eq. 2")
    # try:
    #     s134 = solve_poly_system(set_of_equations134, x, y, z)[0]
    #     z_pos = re(s134[2]) + im(s134[2])
    #     x_pos = s134[0]
    #     y_pos = s134[1]
    #     print("x:{:2.2f} y:{:2.2f} z:{:2.2f}".format(x_pos, y_pos, z_pos))
    #     plt.scatter(x_pos, y_pos)
    #     plt.pause(0.01)
    # except NameError:
    #     print("Failed to solve eq. 3")
    # except NotImplementedError:
    #     print("Failed to solve eq. 3")
    # try:
    #     s234 = solve_poly_system(set_of_equations234, x, y, z)[0]
    #     z_pos = re(s234[2]) + im(s234[2])
    #     x_pos = s234[0]
    #     y_pos = s234[1]
    #     print("x:{:2.2f} y:{:2.2f} z:{:2.2f}".format(x_pos, y_pos, z_pos))
    #     plt.scatter(x_pos, y_pos)
    #     plt.pause(0.01)
    # except NameError:
    #     print("Failed to solve eq. 4")
    # plt.show()
