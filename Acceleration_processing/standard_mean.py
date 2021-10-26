from data_processing import Samples, reading_acc_data, clerification, normalization, SimCos
import numpy as np
from math import sqrt

samples_a = []
samples_t = []
time_length = 1.2
[time_sample,ax_sample,ay_sample,az_sample,a_sample] = Samples("Data/running_pocket_1.csv",time_length)
samples_a+=a_sample[12:45]
samples_t+=time_sample[12:45]
[time_sample,ax_sample,ay_sample,az_sample,a_sample] = Samples("Data/running_pocket_2.csv",time_length)
samples_a+=a_sample[12:45]
samples_t+=time_sample[12:45]
[time_sample,ax_sample,ay_sample,az_sample,a_sample] = Samples("Data/running_pocket_3.csv",time_length)
samples_a+=a_sample[12:42]
samples_t+=time_sample[12:42]
[time_sample,ax_sample,ay_sample,az_sample,a_sample] = Samples("Data/running_pocket_4.csv",time_length)
samples_a+=a_sample[13:45]
samples_t+=time_sample[13:45]

file = open("export_running.lor","w")

for i in range(len(samples_a)):
	for j in range(len(samples_a[i])):
		file.write(str(samples_a[i][j])+"\n")

file.close()

av = []
sd = []
for i in range(len(samples_a)):
	av.append(sum(samples_a[i])/len(samples_a[i]))

for i in range(len(samples_a)):
	s = 0.0
	for j in range(len(samples_a[i])):
		s+=(samples_a[i][j]-av[i])**2
	sd.append(sqrt(s/(len(samples_a[i])-1)))

x = []
y_p = []
y_n = []

for i in range(len(av)):
	x.append(i)
	y_p.append(av[i]+sd[i])
	y_n.append(av[i]-sd[i])

import matplotlib.pyplot as plt 

plt.figure(figsize=(8,8))

plt.plot(av,'r.')
plt.show()