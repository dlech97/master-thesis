import numpy as np
from matplotlib import pyplot as plt

filename = 'acc_test_V2_30cm_Y_only_with_quality.txt'

ignore_lines = True

x_acc = 0
y_acc = 0
z_acc = 0
q_acc = 0

line_counter = 0

avg_positions = list()
avg_quality = list()
y_axis_pos = list()

diff_list = list()

with open(filename) as file:
	lines = file.readlines()
	for line in lines:
		parse = line.split(sep=' ')
		# print(parse)
		if parse[2] == "STOP":
			ignore_lines = True
			print("Ignoring lines")
		if parse[2] == "RESUME":
			print("Resuming")
			ignore_lines = False
			continue
		if ignore_lines:
			try:
				x_avg = x_acc / float(line_counter)
				y_avg = y_acc / float(line_counter)
				z_avg = z_acc / float(line_counter)
				q_avg = q_acc / float(line_counter)

				print("Averaged position: x:{} y:{} z:{} avg.quality:{}".format(x_avg, y_avg, z_avg, q_avg))

				avg_positions.append((x_avg, y_avg, z_avg))
				avg_quality.append(q_avg)
				y_axis_pos.append(y_avg)
			except Exception as ex:
				None

			x_acc = 0
			y_acc = 0
			z_acc = 0
			q_acc = 0
			line_counter = 0
			continue
		else:
			# print("Processing line")
			if parse[3] == 'nan':
				# print("skipping")
				continue
			x = float(parse[3])
			y = float(parse[4])
			z = float(parse[5])
			q = float(parse[7])
			x_acc += x
			y_acc += y
			z_acc += z
			q_acc += q
			line_counter += 1

for i in range(len(avg_positions)-1):
	pos1 = avg_positions[i]
	pos2 = avg_positions[i+1]
	q1 = avg_quality[i]
	q2 = avg_quality[i+1]
	a_q = (q1 + q2) / 2.0
	diff = tuple(map(lambda a, b: a - b, pos2, pos1))
	diff_list.append(diff)
	print(i, diff, a_q)

avg_diff = np.average(diff_list, axis=0)

ground_truth = [0, 0.3, 0]

print(avg_diff)

MAE = []

for l1, l2 in zip(ground_truth, avg_diff):
	print("{:2.2f}".format(100*abs(l2-l1)))
	# MAE.append(100*abs(l2+l1))

plt.plot(y_axis_pos, avg_quality)
plt.show()

