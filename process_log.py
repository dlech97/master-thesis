import numpy as np
from matplotlib import pyplot as plt


def smooth(data, box_pts):
	box = np.ones(box_pts)/box_pts
	data_smooth = np.convolve(data, box, mode='same')
	return data_smooth


filename = 'limited'

ignore_lines = True

x_min = np.inf
x_max = -np.inf
y_min = np.inf
y_max = -np.inf
z_min = np.inf
z_max = -np.inf

mins = list()
maxes = list()

max_list = list()
min_list = list()

x_acc = 0
y_acc = 0
z_acc = 0
q_acc = 0

line_counter = 0
samples_counter = 0

avg_positions = list()
avg_quality = list()
y_axis_pos = list()

diff_list = list()

with open(filename) as file:
	lines = file.readlines()
	for line in lines:
		parse = line.split(sep=' ')
		if parse[2] == "STOP":
			ignore_lines = True
			continue
		if parse[2] == "RESUME":
			ignore_lines = False
			continue
		if ignore_lines:
			try:
				x_avg = x_acc / float(line_counter)
				y_avg = y_acc / float(line_counter)
				z_avg = z_acc / float(line_counter)
				q_avg = q_acc / float(line_counter)

				# print("Averaged position: x:{:2.2f} y:{:2.2f} z:{:2.2f} avg.quality:{:2.2f}".format(x_avg, y_avg, z_avg, q_avg))

				avg_positions.append((x_avg, y_avg, z_avg))
				avg_quality.append(q_avg)
				y_axis_pos.append(y_avg)

				maxes.append((x_max, y_max, z_max))
				mins.append((x_min, y_min, z_min))

			except Exception as ex:
				None

			x_acc = 0
			y_acc = 0
			z_acc = 0
			q_acc = 0
			line_counter = 0

			x_min = np.inf
			x_max = -np.inf
			y_min = np.inf
			y_max = -np.inf
			z_min = np.inf
			z_max = -np.inf

			continue
		else:
			if parse[3] == 'nan':
				continue
			samples_counter += 1
			x = float(parse[3])
			y = float(parse[4])
			z = float(parse[5])
			q = float(parse[7])
			x_acc += x
			y_acc += y
			z_acc += z
			q_acc += q
			line_counter += 1

			if x > x_max:
				x_max = x
			if x < x_min:
				x_min = x
			if y > y_max:
				y_max = y
			if y < y_min:
				y_min = y
			if z > z_max:
				z_max = z
			if z < z_min:
				z_min = z

diff_list.append((0, 0, 0))

for i in range(len(avg_positions)-1):
	pos1 = avg_positions[i]
	max_e = maxes[i]
	min_e = mins[i]
	pos2 = avg_positions[i+1]
	q1 = avg_quality[i]
	q2 = avg_quality[i+1]
	a_q = (q1 + q2) / 2.0
	diff = tuple(map(lambda a, b: a - b, pos2, pos1))
	max_err = tuple(map(lambda a, b: np.abs(a-b), max_e, pos1))
	min_err = tuple(map(lambda a, b: np.abs(a-b), min_e, pos1))
	diff_list.append(diff)
	max_list.append(max_err)
	min_list.append(min_err)
	print("Sample:{} difference:{} quality:{}".format(i, diff, a_q))

avg_diff = np.average(diff_list[1:], axis=0)

ground_truth = [0, 0.3, 0]

print("Average difference:", avg_diff)

print("Samples counter: ", samples_counter)

for l1, l2 in zip(ground_truth, avg_diff):
	print("Error: {:2.5f} cm".format(100*np.abs(l2-l1)))

plt.plot(max_list)
plt.show()

print(np.average(max_list, axis=0))
print(np.average(min_list, axis=0))

plt.plot(min_list)
plt.show()

plt.plot(maxes, linewidth=2)
plt.plot(mins, linewidth=2)
plt.axis([0, 36, -1, 11])
plt.axis([0, 65, -3, 17])
plt.legend(["Oś X - szerokość", "Oś Y - długość", "Oś Z - wysokość"], fontsize='xx-large')
plt.xlabel("Numer próbki", fontsize='xx-large')
plt.ylabel("Wartość próbki [m]", fontsize='xx-large')
plt.show()

plt.plot(y_axis_pos, avg_quality, color="black", linewidth=2)
plt.axis([-2.7, 16, 45, 95])
plt.xlabel("Oś Y [m]", fontsize='xx-large')
plt.ylabel("Jakość pozycji [%]")
plt.plot((0, 0), (45, 100), color='green', linewidth=3)
plt.plot((10.8, 10.8), (45, 100), color='green', linewidth=3)
plt.legend(["Jakość pozycji [%]", "Położenie anchorów"], fontsize='xx-large')
plt.show()
