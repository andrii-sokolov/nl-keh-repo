from os import listdir
from os.path import isfile, join
import csv
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels as sm

def linaprox(y2,y1,x2,x1,x):
	# helpfull function for the linear approximation on two points
	if(x2!=x1):
		A = (y2 - y1)/(x2 - x1)
		B = (y1*x2 - y2*x1)/(x2 - x1)
		return(A*x + B)
	else:
		return(y2)

class processed_data:
	# Takes initial experimental 
	# data files and supplements them with
	# linearly interpolated data
	def __init__(self, folder_name):
		# getting all names from the folder controlled by the <folder_name>
		self.onlyfiles = [f for f in listdir(folder_name) if ((isfile(join(folder_name, f)))&(f[:8]!='sampled_'))]
		# name of a folder with *.csv experimental data
		self.folder_name = folder_name
		# tuple with time
		self.time = []
		# tuple with ax
		self.ax = []
		# tuple with ay
		self.ay = []
		# tuple with az
		self.az = []
		# tuple with acceleration
		self.a = []

	def reading(self):
		# reading files from folder
		temp_time = []
		temp_ax = []
		temp_ay = []
		temp_az = []
		temp_a = []
		for filename in self.onlyfiles:
			temp_time.append([])
			temp_ax.append([])
			temp_ay.append([])
			temp_az.append([])
			temp_a.append([])
			with open(self.folder_name+"/"+filename) as csvfile:
				lines = csv.reader(csvfile, delimiter = ",")
				for row in lines:
					try:
						temp_time[-1].append(float(row[0]))
						temp_ax[-1].append(float(row[1]))
						temp_ay[-1].append(float(row[2]))
						temp_az[-1].append(float(row[3]))
						temp_a[-1].append(float(row[4]))
					except(ValueError):
						pass
		
		for i in range(len(temp_time)):
			self.time.append([])
			self.ax.append([])
			self.ay.append([])
			self.az.append([])
			self.a.append([])
			for j in range(len(temp_time[i])-1):
				if(temp_time[i][j]!=temp_time[i][j+1]):
					self.time[-1].append(temp_time[i][j])
					self.ax[-1].append(temp_ax[i][j])
					self.ay[-1].append(temp_ay[i][j])
					self.az[-1].append(temp_az[i][j])
					self.a[-1].append(temp_a[i][j])

	def suppliment(self):
		# supplementing the data
		dts = []
		for i in range(len(self.time)):
			dt = self.time[i][1]-self.time[i][0]
			for j in range(len(self.time[i])-1):
				if( dt>=self.time[i][j+1]-self.time[i][j] ):
					dt = self.time[i][j+1]-self.time[i][j]
			dts.append(round(dt,4))
		
		temp_time = []
		temp_ax = []
		temp_ay = []
		temp_az = []
		temp_a = []

		for i in range(len(self.time)):
			print(self.onlyfiles[i])
			temp_time.append([])
			temp_ax.append([])
			temp_ay.append([])
			temp_az.append([])
			temp_a.append([])
			t = self.time[i][0]
			while(t<self.time[i][-1]):
				t += dts[i]
				j_min = 0
				j_max = len(self.time[i])-1
				try:
					while(self.time[i][j_min] < t):
						j_min+=1
				except IndexError:
					j_min = len(self.time[i]) -1
				while(self.time[i][j_max] > t):
					j_max-=1
				
				temp_time[-1].append(t)
				temp_ax[-1].append(linaprox(self.ax[i][j_max],self.ax[i][j_min],self.time[i][j_max],self.time[i][j_min],t))
				temp_ay[-1].append(linaprox(self.ay[i][j_max],self.ay[i][j_min],self.time[i][j_max],self.time[i][j_min],t))
				temp_az[-1].append(linaprox(self.az[i][j_max],self.az[i][j_min],self.time[i][j_max],self.time[i][j_min],t))
				temp_a[-1].append(linaprox(self.a[i][j_max],self.a[i][j_min],self.time[i][j_max],self.time[i][j_min],t))
		
		self.time = temp_time
		self.ax = temp_ax
		self.ay = temp_ay
		self.az = temp_az
		self.a = temp_a

	def write_files(self):
		# writing files
		for i in range(len(self.time)):
			file = open(self.folder_name+"/sampled_"+self.onlyfiles[i],'w')
			for j in range(len(self.time[i])):
				file.write(str(self.time[i][j])+","+str(self.ax[i][j])+","+str(self.ay[i][j])+","+str(self.az[i][j])+","+str(self.a[i][j])+"\n")
			file.close()


class preprocessed_data_sample:
	# class for the postprocessing of  
	# the preprocessed experimental data
	def __init__(self, folder_name):
		self.onlyfiles = [f for f in listdir(folder_name) if ((isfile(join(folder_name, f)))&(f[:8]=='sampled_'))]
		self.init_dataframes = []
		for filename in self.onlyfiles:
			self.init_dataframes.append(pd.read_csv(folder_name+'/'+filename, names = ['time','ax','ay','az','a'], index_col = 0, squeeze=True))

		self.time = []
		self.ax = []
		self.ay = []
		self.az = []
		self.a = []
		
		for dataframe in self.init_dataframes:
			self.time.append(list(dict(dataframe['ax']).keys()))
			self.ax.append(list(dict(dataframe['ax']).items()))
			self.ay.append(list(dict(dataframe['ay']).items()))
			self.az.append(list(dict(dataframe['az']).items()))
			self.a.append(list(dict(dataframe['a']).items()))			

		self.end_dataframes = []

	def sampling_n(self, n_points):
		temp_t = []
		temp_ax = []
		temp_ay = []
		temp_az = []
		temp_a = []

		temp_df = []
		for i in range(len(self.time)):
			dt = (self.time[i][-1] - self.time[i][0])/n_points
			t0 = self.time[i][0]
			t = 0

			temp_t.append([])
			temp_ax.append([])
			temp_ay.append([])
			temp_az.append([])
			temp_a.append([])

			while( t<self.time[i][-1] ):
				
				j_min = 0
				j_max = len(self.time[i])-1
				
				try:
					while(self.time[i][j_min] < (t+t0)):
						j_min+=1
				except IndexError:
					j_min = len(self.time[i]) -1
				try:
					while(self.time[i][j_max] > (t+t0)):
						j_max-=1
				except IndexError:
					pass

				temp_t[-1].append(t)
				temp_ax[-1].append(linaprox(self.ax[i][j_max][1],self.ax[i][j_min][1],self.time[i][j_max],self.time[i][j_min],t+t0))
				temp_ay[-1].append(linaprox(self.ay[i][j_max][1],self.ay[i][j_min][1],self.time[i][j_max],self.time[i][j_min],t+t0))
				temp_az[-1].append(linaprox(self.az[i][j_max][1],self.az[i][j_min][1],self.time[i][j_max],self.time[i][j_min],t+t0))
				temp_a[-1].append(linaprox(self.a[i][j_max][1],self.a[i][j_min][1],self.time[i][j_max],self.time[i][j_min],t+t0))

				t+=dt

			temp_df.append(pd.DataFrame({'time':temp_t[-1], 'ax':temp_ax[-1], 'ay':temp_ay[-1], 'az':temp_az[-1], 'a':temp_a[-1]}))
			temp_df[-1] = temp_df[-1].set_index('time')

		return(temp_df)

	def sampling_dt(self, dt):
		temp_t = []
		temp_ax = []
		temp_ay = []
		temp_az = []
		temp_a = []

		temp_df = []
		for i in range(len(self.time)):
			dt = dt
			t0 = self.time[i][0]
			t = 0

			temp_t.append([])
			temp_ax.append([])
			temp_ay.append([])
			temp_az.append([])
			temp_a.append([])

			while( t<self.time[i][-1] ):
				
				j_min = 0
				j_max = len(self.time[i])-1
				
				try:
					while(self.time[i][j_min] < (t+t0)):
						j_min+=1
				except IndexError:
					j_min = len(self.time[i]) -1
				try:
					while(self.time[i][j_max] > (t+t0)):
						j_max-=1
				except IndexError:
					pass

				temp_t[-1].append(t)
				temp_ax[-1].append(linaprox(self.ax[i][j_max][1],self.ax[i][j_min][1],self.time[i][j_max],self.time[i][j_min],t+t0))
				temp_ay[-1].append(linaprox(self.ay[i][j_max][1],self.ay[i][j_min][1],self.time[i][j_max],self.time[i][j_min],t+t0))
				temp_az[-1].append(linaprox(self.az[i][j_max][1],self.az[i][j_min][1],self.time[i][j_max],self.time[i][j_min],t+t0))
				temp_a[-1].append(linaprox(self.a[i][j_max][1],self.a[i][j_min][1],self.time[i][j_max],self.time[i][j_min],t+t0))

				t+=dt

			temp_df.append(pd.DataFrame({'time':temp_t[-1], 'ax':temp_ax[-1], 'ay':temp_ay[-1], 'az':temp_az[-1], 'a':temp_a[-1]}))
			temp_df[-1] = temp_df[-1].set_index('time')

		return(temp_df)