from data_processing import Samples, reading_acc_data, clerification, normalization, SimCos
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tftb.processing import ShortTimeFourierTransform
import numpy as np

data_pool_t = []
data_pool_a = []

[t,ax,ay,az,a] = reading_acc_data("Data/running_pocket_1.csv")
[t_cl,ax_cl,ay_cl,az_cl,a_cl] = clerification([t,ax,ay,az,a])
[t_norm, a_x_norm, a_y_norm, a_z_norm, a_norm,dtime] = normalization([t_cl,ax_cl,ay_cl,az_cl,a_cl])
data_pool_t.append(t_norm)
data_pool_a.append(a_norm)
print(dtime)

'''
[t,ax,ay,az,a] = reading_acc_data("Data/running_pocket_2.csv")
[t_cl,ax_cl,ay_cl,az_cl,a_cl] = clerification([t,ax,ay,az,a])
[t_norm, a_x_norm, a_y_norm, a_z_norm, a_norm,dtime] = normalization([t_cl,ax_cl,ay_cl,az_cl,a_cl])
data_pool_t.append(t_norm)
data_pool_a.append(a_norm)
print(dtime)

[t,ax,ay,az,a] = reading_acc_data("Data/running_pocket_3.csv")
[t_cl,ax_cl,ay_cl,az_cl,a_cl] = clerification([t,ax,ay,az,a])
[t_norm, a_x_norm, a_y_norm, a_z_norm, a_norm,dtime] = normalization([t_cl,ax_cl,ay_cl,az_cl,a_cl])
data_pool_t.append(t_norm)
data_pool_a.append(a_norm)
print(dtime)

[t,ax,ay,az,a] = reading_acc_data("Data/running_pocket_4.csv")
[t_cl,ax_cl,ay_cl,az_cl,a_cl] = clerification([t,ax,ay,az,a])
[t_norm, a_x_norm, a_y_norm, a_z_norm, a_norm,dtime] = normalization([t_cl,ax_cl,ay_cl,az_cl,a_cl])
data_pool_t.append(t_norm)
data_pool_a.append(a_norm)
print(dtime)
'''

ex_file = open("export_acceleration_sample.lor","w")
export_graph = []

for i in range(len(data_pool_a)):
	for j in range(len(data_pool_a[i])):
		if((data_pool_t[i][j]>20)&(data_pool_t[i][j]<45)):
			ex_file.write(str(data_pool_a[i][j])+"\n")
			export_graph.append(data_pool_a[i][j])
ex_file.close()

from scipy import signal

sos = signal.butter(10, 40.0, 'lp', fs=1000, output='sos')
filtered = signal.sosfilt(sos, export_graph)

print(len(export_graph))

plt.plot(export_graph)
plt.plot(filtered)
plt.show()

export_graph = filtered

def build_portrait(i_shift):
	export_1 = []
	export_2 = []
	export_3 = []
	for i in range( len(export_graph)-2*i_shift):
		export_1.append(export_graph[i])
		export_2.append(export_graph[i + i_shift])
		export_3.append(export_graph[i + 2*i_shift])

	import matplotlib as mpl
	from mpl_toolkits.mplot3d import Axes3D
	import numpy as np
	import matplotlib.pyplot as plt

	fig = plt.figure()
	ax = fig.gca(projection='3d')



	ax.scatter(export_1, export_2, export_3,'.', label='shift = '+str(i_shift))
	ax.legend()

	plt.savefig('portrait_'+str(i_shift)+'_.png')

def export_portrait(i_shift):
	export_1 = []
	export_2 = []
	export_3 = []
	for i in range( len(export_graph)-2*i_shift):
		export_1.append(export_graph[i])
		export_2.append(export_graph[i + i_shift])
		export_3.append(export_graph[i + 2*i_shift])
	return([export_1,export_2,export_3])



def show_portrait(i_shift):
	export_1 = []
	export_2 = []
	export_3 = []
	for i in range( len(export_graph)-2*i_shift):
		export_1.append(export_graph[i])
		export_2.append(export_graph[i + i_shift])
		export_3.append(export_graph[i + 2*i_shift])

	import matplotlib as mpl
	from mpl_toolkits.mplot3d import Axes3D
	import numpy as np
	import matplotlib.pyplot as plt

	fig = plt.figure()
	ax = fig.gca(projection='3d')



	ax.plot(export_1, export_2, export_3, label='shift = '+str(i_shift))
	ax.legend()

	plt.show()

i = 2
while (i<3000):
	build_portrait(i)
	i+=1
'''
show_portrait(17)
'''
