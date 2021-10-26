import numpy as np
import matplotlib.pyplot as plt
import nolds

from scipy import signal

from data_processing import Samples, reading_acc_data, clerification, normalization, SimCos

Signal = []
'''
filename1 = "Data/running_pocket_1.csv"
filename2 = "Data/running_pocket_2.csv"
filename3 = "Data/running_pocket_3.csv"
filename4 = "Data/running_pocket_4.csv"
'''
filename1 = "Data/walking_left_hand_1.csv"
filename2 = "Data/walking_left_hand_2.csv"
filename3 = "Data/walking_left_hand_3.csv"
filename4 = "Data/walking_left_hand_4.csv"

[t,ax,ay,az,a] = reading_acc_data(filename1)
# The clarification of the data (removing the double points)
[t_cl,ax_cl,ay_cl,az_cl,a_cl] = clerification([t,ax,ay,az,a])
# Normalization of the datasets (complement the inexistant times)
[t_norm, a_x_norm, a_y_norm, a_z_norm, a_norm,dtime] = normalization([t_cl,ax_cl,ay_cl,az_cl,a_cl])
Signal+=a_norm[20000:50000]

[t,ax,ay,az,a] = reading_acc_data(filename2)
# The clarification of the data (removing the double points)
[t_cl,ax_cl,ay_cl,az_cl,a_cl] = clerification([t,ax,ay,az,a])
# Normalization of the datasets (complement the inexistant times)
[t_norm, a_x_norm, a_y_norm, a_z_norm, a_norm,dtime] = normalization([t_cl,ax_cl,ay_cl,az_cl,a_cl])
Signal+=a_norm[10000:50000]

[t,ax,ay,az,a] = reading_acc_data(filename3)
# The clarification of the data (removing the double points)
[t_cl,ax_cl,ay_cl,az_cl,a_cl] = clerification([t,ax,ay,az,a])
# Normalization of the datasets (complement the inexistant times)
[t_norm, a_x_norm, a_y_norm, a_z_norm, a_norm,dtime] = normalization([t_cl,ax_cl,ay_cl,az_cl,a_cl])
Signal+=a_norm[10000:50000]

[t,ax,ay,az,a] = reading_acc_data(filename4)
# The clarification of the data (removing the double points)
[t_cl,ax_cl,ay_cl,az_cl,a_cl] = clerification([t,ax,ay,az,a])
# Normalization of the datasets (complement the inexistant times)
[t_norm, a_x_norm, a_y_norm, a_z_norm, a_norm,dtime] = normalization([t_cl,ax_cl,ay_cl,az_cl,a_cl])
Signal+=a_norm[10000:40000]

plt.subplot(2, 1, 1)
plt.plot(Signal, '-')
plt.title('A tale of 2 subplots')
plt.ylabel('Damped oscillation')

'''
for i in range(len(Signal)):
	Signal[i] -= average
'''

sos = signal.butter(10, 15.0, 'lp', fs=1000, output='sos')
filtered = signal.sosfilt(sos, Signal)

filtered_1 = []
exfile = open("Data_walk.lor","w")

for i in range(len(filtered)):
	exfile.write(str(filtered[i])+"\n")
	if (i%10 == 0):
		filtered_1.append(filtered[i])
exfile.close()

plt.subplot(2, 1, 2)
plt.plot(filtered_1, '-')
plt.xlabel('time (s)')
plt.ylabel('Undamped')

plt.show()
'''
n_shift = 1100
x = []
y = []
for i in range(len(filtered) - n_shift):
	x.append(filtered[i])
	y.append(filtered[i + n_shift])

plt.plot(x,y)
plt.show()
'''

#cd = nolds.corr_dim(filtered_1,3,debug_plot=True)
#print(cd)

print(nolds.lyap_r_len(emb_dim = 12, lag = 120, min_tsep = 3500, trajectory_len = 120))
ed = []
h2 = []
for i in range(1,10):
	ed.append(5*i)
	h2.append( nolds.lyap_r(filtered_1,emb_dim = 5*i, lag = 100, tau = 0.01, min_tsep = 480, trajectory_len = 960, debug_plot = False))
	print(h2)

plt.plot(ed,h2)
plt.show()



#ss = nolds.sampen(filtered_1,emb_dim = 3)
#print(ss)

