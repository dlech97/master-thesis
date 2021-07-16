import socket
from struct import unpack
import time
import numpy as np
from matplotlib import pyplot as plt

sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host, port = '0.0.0.0', 65000
server_address = (host, port)

sckt.bind(server_address)

message, address = sckt.recvfrom(4096)
a1_x, a1_y, a1_z, a2_x, a2_y, a2_z, a3_x, a3_y, a3_z, a4_x, a4_y, a4_z = unpack('12f', message)
a1_pos = (a1_x, a1_y, a1_z)   # 0  0  C
a2_pos = (a2_x, a2_y, a2_z)  # x2  0  C
a3_pos = (a3_x, a3_y, a3_z)  # x3 y3  C
a4_pos = (a4_x, a4_y, a4_z)
print(a1_pos)
time.sleep(3)

plt.figure()
while True:
	message, address = sckt.recvfrom(4096)
	da1, da2, da3, da4 = unpack('4f', message)
	print("A1:{:2.2f} A2:{:2.2f} A3:{:2.2f} A4:{:2.2f}".format(da1, da2, da3, da4))
	x = (da1**2 - da2**2 + a2_x**2) / 2 * a2_x
	y = (da1**2 - da3**2 + a3_x**2 + a3_y**2 - (a3_x*(da1**2 - da2**2 + a2_x**2)) / a2_x) / 2 * a3_y
	z = a1_z - np.sqrt(da1**2 - np.square((da1**2 - da2**2 + a2_x**2) / 2*a2_x) - np.square((da1**2 - da3**2 + a3_x**2 + a3_y**2 - a3_x*((da1**2 - da2**2 + a2_x**2) / a2_x)) / 2*a3_y))
	print("x:{} y:{} z:{}".format(x, y, z))
	plt.scatter(x, y)
	plt.show()
