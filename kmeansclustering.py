import numpy as np
import csv
import matplotlib.pyplot as plt
import random
import math


#function to calculate euclidean distance
def euclidean_dist(p1_x, p1_y, p2_x, p2_y):
	dist = math.sqrt(math.pow((p2_x - p1_x), 2) + math.pow((p2_y - p1_y), 2))
	return dist


#function to recalculate new centres
def recal_new_centres(k, x_data, y_data, x_centres, y_centres):
	x_sum = y_sum = c = 0
	for i in range(k):
		for j in range(100):
			if selected_centre[j] == i:
				x_sum = x_sum + x_data[j]
				y_sum = y_sum + y_data[j]
				c = c + 1
		x_centres[i] = x_sum / c
		y_centres[i] = y_sum / c
		c = x_sum = y_sum = 0
	return x_centres, y_centres


#function to recalcuate distances from centres and selct centres for data accordingly
def recal_dist_selectedcentres(f, x_data, y_data, x_centres, y_centres, dist, selected_centre):
	for i in range(0, k):
		for j in range(100):
			d = euclidean_dist(x_data[j], y_data[j], x_centres[i], y_centres[i])
			if d < dist[j]:
				f = 1
				dist[j] = d
				selected_centre[j] = i
	return f, dist, selected_centre


k = int(input("Enter the number of means(k) :: "))
x_data = np.zeros((100))
y_data = np.zeros((100))
x_centres = np.zeros((k))
y_centres = np.zeros((k))
dist = np.zeros((100))
selected_centre = np.zeros((100))
data_marker = ['ro', 'go', 'bo', 'co', 'mo', 'yo', 'ko']
centre_marker = ['rd', 'gd', 'bd', 'cd', 'md', 'yd', 'kd']
i = 0


#read data from file
with open('data.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		x_data[i] = int(row['x'])
		y_data[i] = int(row['y'])
		i = i + 1


#initializing means
for i in range(k):
	x_centres[i] = random.choice(x_data)
	y_centres[i] = random.choice(y_data)


#calculating initial distances from centres
for i in range(100):
	dist[i] = euclidean_dist(x_data[i], y_data[i], x_centres[0], y_centres[0])
	selected_centre[i] = 0
for i in range(1, k):
	for j in range(100):
		d = euclidean_dist(x_data[j], y_data[j], x_centres[i], y_centres[i])
		if d < dist[j]:
			dist[j] = d
			selected_centre[j] = i


#new centres recalculation
x_centres, y_centres = recal_new_centres(k, x_data, y_data, x_centres, y_centres)

#checking until no data is reassigned to a different centre
f = 1
while f == 1:
	f, dist, selected_centre = recal_dist_selectedcentres(0, x_data, y_data, x_centres, y_centres, dist, selected_centre)
	x_centres, y_centres = recal_new_centres(k, x_data, y_data, x_centres, y_centres)


#plotting data and means
for i in range(k):
	for j in range(100):
		if selected_centre[j] == i:
			plt.plot(x_data[j], y_data[j], data_marker[i])
	plt.plot(x_centres[i], y_centres[i], centre_marker[i], ms=10.0)
plt.axis([0, 200, 0, 200])
plt.show()
