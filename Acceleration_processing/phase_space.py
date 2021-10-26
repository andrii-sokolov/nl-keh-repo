from data_processing import Samples, reading_acc_data, clerification, normalization, SimCos
import numpy as np


def Phase_portrait( filename, tau ):
	[t,ax,ay,az,a] = reading_acc_data(filename)
	[t_cl,ax_cl,ay_cl,az_cl,a_cl] = clerification([t,ax,ay,az,a])
	[t_norm, a_x_norm, a_y_norm, a_z_norm, a_norm,dtime] = normalization([t_cl,ax_cl,ay_cl,az_cl,a_cl])
	i_tau = 0
	for i in range(len(t_norm)):
		if( t_norm[i] > tau):
			i_tau = i
			break
	a_export_1 = []
	a_export_2 = []
	for i in range(len(a_norm)-i_tau):
		a_export_1.append(a_norm[i])
		a_export_2.append(a_norm[i+i_tau])
	return([a_export_1, a_export_2])

def Draw_phase_portrait(filename, tau):
	[a1,a2] =Phase_portrait("Data/walking_left_hand_1.csv" ,1.3 )
	import matplotlib.pyplot as plt 
	plt.plot(a1,a2)
	plt.show() 

def norm(x,y):
	try:
		ans = 0.0
		for i in range(len(x)):
			ans += (x[i] - y[i])**2
		return ( ans**0.5 )
	except:
		return(0.0)

def CorrelationIntergral(filename, epsilon, m):
	[t,ax,ay,az,a] = reading_acc_data(filename)
	[t_cl,ax_cl,ay_cl,az_cl,a_cl] = clerification([t,ax,ay,az,a])
	[t_norm, a_x_norm, a_y_norm, a_z_norm, a_norm,dtime] = normalization([t_cl,ax_cl,ay_cl,az_cl,a_cl])
	summ = 0.0
	for i in range(len(a_norm) - m):
		for j in range(len(a_norm) - m):
			summ+= np.heaviside(epsilon - norm(a_norm[i:i+m],a_norm[j:j+m]),0.5)
	return(summ/((len(a_norm)-m)*(len(a_norm)-m-1)))

def increasing_sum(filename, index, tau, epsilon):
	#Rosenstein - Kantz algorithm
	[t,ax,ay,az,a] = reading_acc_data(filename)
	[t_cl,ax_cl,ay_cl,az_cl,a_cl] = clerification([t,ax,ay,az,a])
	[t_norm, a_x_norm, a_y_norm, a_z_norm, a_norm,dtime] = normalization([t_cl,ax_cl,ay_cl,az_cl,a_cl])
	x_in_epsilon=[]
	t_in_epsilon=[]
	for i in range(len(a_norm)):
		if(abs(a_norm[index] - a_norm[i])<epsilon):
			x_in_epsilon.append(a_norm[i])
			t_in_epsilon.append(t_norm[i])
	Sum = 0.0
	k = 0
	for i in range(len(x_in_epsilon)):
		for j in range(len(t_norm)):
			if ((t_norm[j] - t_in_epsilon[i])>tau):
				Sum += abs(x_in_epsilon[i]-a_norm[j])
				k+=1
				break
	return(Sum/k)

def S(filename,tau, imax):
	Sum = 0.0
	for i in range(imax):
		Sum += increasing_sum(filename,i, tau, 0.001)
		#print(str(i)+"\t"+str(Sum))
	return(Sum/imax)

tau = 0.1
while (tau<10.0):
	print(S("Data/walking_left_hand_1.csv", tau, 100))
	tau+=0.1

#print(CorrelationIntergral("Data/walking_left_hand_1.csv", 0.1, 2500))