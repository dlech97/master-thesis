import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import PySimpleGUI as sg

filename = 'testing 2 tags.txt'
NUMBER_OF_TAGS = 2
data_valid = False

matplotlib.use("TkAgg")


def draw_figure_w_toolbar(canvas, fig):
	if canvas.children:
		for child in canvas.winfo_children():
			child.destroy()
	figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
	figure_canvas_agg.get_tk_widget().forget()
	plt.close("all")
	figure_canvas_agg.draw()
	figure_canvas_agg.get_tk_widget().pack(side='right', fill='both', expand=1)


# def draw_figure(canvas, figure):
# 	figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
# 	figure_canvas_agg.get_tk_widget().forget()
# 	plt.close('all')
# 	figure_canvas_agg.draw()
# 	figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
# 	return figure_canvas_agg


def smooth(data, box_pts):
	box = np.ones(box_pts) / box_pts
	data_smooth = np.convolve(data, box, mode='same')
	return data_smooth


list_tag = list()
list_x = list()
list_y = list()
list_z = list()
list_timestamp = list()

with open(filename) as file:
	lines = file.readlines()
	for line in lines:
		parse = line.split(sep=' ')
		if parse[2] == 'STOP':
			data_valid = False
		elif parse[2] == "RESUME":
			data_valid = True
		else:
			if parse[5] == 'nan':
				continue
			if data_valid:
				x = float(parse[5])
				y = float(parse[6])
				z = float(parse[7])
				q = float(parse[9])
				list_tag.append(parse[3])
				list_x.append(x)
				list_y.append(y)
				list_z.append(z)
				list_timestamp.append(parse[1])

# # # acceleration calculation # NOT WORKING
# for i in range(len(speeds) - 1):
# 	sx1, sy1, sz1 = speeds[i]
# 	sx2, sy2, sz2 = speeds[i + 1]
# 	acc_x = (sx2 - sx1) / 0.1
# 	acc_y = (sy2 - sy1) / 0.1
# 	acc_z = (sz2 - sz1) / 0.1
#
# 	origin = np.array([sx[i], sy[i]])
# 	plt.quiver(*origin, acc_x, acc_y, scale=800)

list_of_tag_names = [list_tag[i] for i in range(NUMBER_OF_TAGS)]
list_of_tag_positions = np.zeros((NUMBER_OF_TAGS, int(len(list_x)/NUMBER_OF_TAGS)), dtype=object)

# SPLIT POSITIONS TAG-WISE
k = 0
for i in range(len(list_x)):
	for t in range(NUMBER_OF_TAGS):
		if i % NUMBER_OF_TAGS == t:
			list_of_tag_positions[t, k] = (list_x[i], list_y[i], list_z[i])
	if i % NUMBER_OF_TAGS == NUMBER_OF_TAGS-1:
		k += 1
	if k >= int(len(list_x)/NUMBER_OF_TAGS):
		break

print(list_timestamp)
# print(list_of_tag_positions)
# print(list_of_tag_names)
# print(len(list_x)/2)

TAIL = 10

layout = [[sg.Canvas(key='-CANVAS-')],
		[sg.Slider(range=(1, 30), default_value=1, size=(20, 30), orientation='h', key='smooth_slider', enable_events=True)],
		[sg.Slider(range=(TAIL, int(len(list_x)/NUMBER_OF_TAGS)-TAIL), default_value=TAIL, size=(20, 30), orientation='h', key='position_slider', enable_events=True)],
		[sg.Checkbox('Show full trajectory', default=True, key='full_traj')],
		[sg.Checkbox('3D plot', default=True, key='3d_plot')],
		[sg.Button("Show")],
		[sg.Checkbox(list_of_tag_names[i], default=True, key=list_of_tag_names[i]) for i in range(NUMBER_OF_TAGS)]]

main_window = sg.Window(title="GUI", layout=layout, finalize=True, location=(0, 0))

smoothing_factor = 1
pos = 0

while True:
	event, values = main_window.read()
	if event == sg.WIN_CLOSED:
		break

	if event == 'smooth_slider':
		smoothing_factor = int(values['smooth_slider'])

	fig = Figure(figsize=(10, 7))
	if values['3d_plot']:
		ax = fig.add_subplot(111, projection='3d')
	else:
		ax = fig.add_subplot(111)

	tag_selected = False

	legend = []
	for tag_name in list_of_tag_names:
		if values[tag_name]:
			legend.append(tag_name)

	for i in range(NUMBER_OF_TAGS):
		if values[list_of_tag_names[i]]:
			tag_selected = True
			# print(list_of_tag_positions[i])
			sx = [list_of_tag_positions[i][it][0] for it in range(len(list_of_tag_positions[i]))]
			sy = [list_of_tag_positions[i][it][1] for it in range(len(list_of_tag_positions[i]))]
			sz = [list_of_tag_positions[i][it][2] for it in range(len(list_of_tag_positions[i]))]

			# SMOOTHING
			sx = smooth(sx, smoothing_factor)
			sy = smooth(sy, smoothing_factor)
			sz = smooth(sz, smoothing_factor)

			if values['3d_plot']:
				if event == 'position_slider':
					pos = int(values['position_slider'])

				if values['full_traj']:

					x = sx
					y = sy
					z = sz

				else:

					x = [sx[i] for i in range(pos-int(TAIL/2), pos+int(TAIL/2))]
					y = [sy[i] for i in range(pos-int(TAIL/2), pos+int(TAIL/2))]
					z = [sz[i] for i in range(pos-int(TAIL/2), pos+int(TAIL/2))]
					time = list_timestamp[NUMBER_OF_TAGS * pos]
					ax.text(x=0, y=0, z=0, s=time)

				ax.plot(x, y, z, '.--', linewidth=0.5)
				ax.set_xlabel('Oś X - szerokość [m]')
				ax.set_ylabel('Oś Y - długość [m]')
				ax.set_zlabel('Oś Z - wysokość [m]')
				ax.set_xlim3d(0, 3)
				ax.set_ylim3d(-1, 12)
				ax.set_zlim3d(0, 2)
				ax.legend(legend)
				draw_figure_w_toolbar(main_window['-CANVAS-'].TKCanvas, fig)
				main_window.Refresh()
			else:
				# fig = Figure(figsize=(10, 7))
				ax.plot(sx, sy, '.--')
				speeds = list()

				for i in range(len(sx) - 1):  # speed calculation
					x1 = sx[i]
					x2 = sx[i + 1]
					speed_x = (x2 - x1) / 0.1
					y1 = sy[i]
					y2 = sy[i + 1]
					speed_y = (y2 - y1) / 0.1
					z1 = sz[i]
					z2 = sz[i + 1]
					speed_z = (z2 - z1) / 0.1
					# print("Speed vector: (x,y)=({:2.2f},{:2.2f}) m/s".format(speed_x, speed_y))

					speeds.append((speed_x, speed_y, speed_z))

					origin = np.array([x1, y1])
					ax.quiver(*origin, speed_x, speed_y, scale=100, color='red')

				legend = []
				for tag_name in list_of_tag_names:
					if values[tag_name]:
						legend.append(tag_name)
				legend.append("Speed vector")
				ax.legend(legend)
				# plt.axis([-3, 5, -3, 18])
				# ax.xlabel("Oś X - szerokość [m]", fontsize='xx-large')
				# ax.ylabel("Oś Y - długość [m]", fontsize='xx-large')
				draw_figure_w_toolbar(main_window['-CANVAS-'].TKCanvas, fig)
				main_window.Refresh()
	if tag_selected is False:
		sg.popup_error("No tag selected! Please select at least one tag")

main_window.close()

# # 2 dimensional plot X-Y
# plt.plot(sx, sy, '.k--')

# for i in range(len(list_x) - 1):  # speed calculation
# 	x1 = sx[i]
# 	x2 = sx[i + 1]
# 	speed_x = (x2 - x1) / 0.1
# 	y1 = sy[i]
# 	y2 = sy[i + 1]
# 	speed_y = (y2 - y1) / 0.1
# 	z1 = sz[i]
# 	z2 = sz[i + 1]
# 	speed_z = (z2 - z1) / 0.1
# 	# print("Speed vector: (x,y)=({:2.2f},{:2.2f}) m/s".format(speed_x, speed_y))
#
# 	speeds.append((speed_x, speed_y, speed_z))
#
# 	origin = np.array([x1, y1])
# 	plt.quiver(*origin, speed_x, speed_y, scale=200, color='red')
# plt.legend(["Lokalizacja", "Wektor prędkości"])
# # plt.axis([-3, 5, -3, 18])
# plt.xlabel("Oś X - szerokość [m]", fontsize='xx-large')
# plt.ylabel("Oś Y - długość [m]", fontsize='xx-large')
# plt.show()
#
# # 3 dimensional plot
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot(sx, sy, sz, '.r--', linewidth=1)
# ax.set_xlabel('Oś X - szerokość [m]')
# ax.set_ylabel('Oś Y - długość [m]')
# ax.set_zlabel('Oś Z - wysokość [m]')
# ax.set_xlim3d(-3, 6)
# ax.set_ylim3d(-5, 15)
# ax.set_zlim3d(0, 2)
# plt.show()
