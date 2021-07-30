import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import BSpline

filename = 'running_7.txt'


def smooth(data, box_pts):
	box = np.ones(box_pts)/box_pts
	data_smooth = np.convolve(data, box, mode='same')
	return data_smooth


# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

list_x = list()
list_y = list()
list_z = list()

with open(filename) as file:
	lines = file.readlines()
	for line in lines:
		parse = line.split(sep=' ')
		if parse[2] == "STOP":
			continue
		if parse[2] == "RESUME":
			continue
		else:
			if parse[3] == 'nan':
				continue
			x = float(parse[3])
			y = float(parse[4])
			z = float(parse[5])
			q = float(parse[7])
			list_x.append(x)
			list_y.append(y)
			list_z.append(z)

# speed calculation
for i in range(len(list_x) - 1):
	x1 = list_x[i]
	x2 = list_x[i + 1]
	speed_x = (x2 - x1) / 0.1
	y1 = list_y[i]
	y2 = list_y[i + 1]
	speed_y = (y2 - y1) / 0.1
	print("Speed vector: (x,y)=({:2.2f},{:2.2f}) m/s".format(speed_x, speed_y))

	origin = np.array([x1, y1])
	plt.quiver(*origin, speed_x, speed_y, scale=100)

# # 2 dimensional plot X-Y
plt.plot(list_x, list_y, color='g')
plt.plot(smooth(list_x, 5), smooth(list_y, 5))
plt.show()

# # 3 dimensional plot
# ax.plot(list_x, list_y, list_z)
# ax.set_xlim3d(-5, 5)
# ax.set_ylim3d(-5, 15)
# ax.set_zlim3d(0, 2)
# plt.show()
