import csv                #importing library for *.csv files processing
from math import sqrt     #importing sqrt function from math library

def reading_acc_data(filename):
    '''
    The method reads the accelerometer data from <filename> csv file
    and returns it in form:
    [<time>, <x-acceleration>, <y-acceleration>, <z-acceleration>, <module acceleration>]
    '''
    time  = []      #time sequence
    acc_x = []      #x-acceleration sequence
    acc_y = []      #y-acceleration sequence
    acc_z = []      #z-acceleration sequence
    acc   = []      #module acceleration
    with open(filename) as datafile:                     #opening given *.csv file
        datareader = csv.reader(datafile, delimiter=",") #setting separation symbol as ','
        for line in datareader:                          #writing the data on prepeared lists: 
            try:
                time.append(float(line[0]))
                acc_x.append(float(line[1]))
                acc_y.append(float(line[2]))
                acc_z.append(float(line[3]))
                acc.append(float(line[4]))
            except(ValueError):
                pass
    return([time,acc_x,acc_y,acc_z,acc]) #returning of the final answer

def clerification(data):
    export_data_time = []
    export_data_ax = []
    export_data_ay = []
    export_data_az = []
    export_data_a = []
    for i in range(1,len(data[0])):
        if (data[0][i] == data[0][i-1]):
            pass
        else:
            export_data_time.append(data[0][i])
            export_data_ax.append(data[1][i])
            export_data_ay.append(data[2][i])
            export_data_az.append(data[3][i])
            export_data_a.append(data[4][i])
    return([export_data_time,export_data_ax,export_data_ay,export_data_az,export_data_a])

def interp3(y1,y2,y3,t1,t2,t3,t):
    A = ((t2-t1)*y3 + (t1-t3)*y2 + (t3-t2)*y1)/((t2-t1)*t3**2 + (t1**2 - t2**2)*t3 + t1*t2**2 - t1**2*t2)
    B = -((t2**2 - t1**2)*y3 + (t1**2 - t3**2)*y2 + (t3**2 - t2**2)*y1)/((t2-t1)*t3**2 + (t1**2 - t2**2)*t3 + t1*t2**2 - t1**2*t2)
    C = ((t1*t2**2 - t1**2*t2)*y3 + (t1**2*t3 - t1*t3**2)*y2 + (t2*t3**2 - t2**2*t3)*y1)/((t2-t1)*t3**2 + (t1**2 - t2**2)*t3 + t1*t2**2 - t1**2*t2)
    return(A*t**2 + B*t + C)

def interp2(y1,y2,t1,t2,t):
    B = (y2-y1)/(t2-t1)
    C = -(t1*y2 - t2*y1)/(t2-t1)
    return( B*t + C)

def normalization(data):
#function normalises the data-set (interpolates skipped itme-points)
#EXAMPLE: ns_data = normalization(s_data[0][3],s_data[1][3])
    
    #Define the minimal step by the time 
    dt = data[0][1] - data[0][0]    
    for i in range(1,len(data[0])):
        if(dt>data[0][i]-data[0][i-1]):
            dt = round(data[0][i] - data[0][i-1],4)

    export_t = [data[0][0]]         #list for the time sequences
    export_ax =[data[1][0]]         #list for the acceleration sequences
    export_ay =[data[2][0]]         #list for the acceleration sequences
    export_az =[data[3][0]]         #list for the acceleration sequences
    export_a  =[data[4][0]]         #list for the acceleration sequences

    for i in range(1,len(data[0])):
        if(round(data[0][i]-export_t[-1],4)==dt):
            export_t.append(data[0][i])
            export_ax.append(data[1][i])
            export_ay.append(data[2][i])
            export_az.append(data[3][i])
            export_a.append(data[4][i])
        else:
            while(round(data[0][i]-export_t[-1],4)>=dt):
                export_t.append (round(export_t[-1]+dt,4))
                export_ax.append(interp2(data[1][i-1],data[1][i],data[0][i-1],data[0][i],export_t[-1]))
                export_ay.append(data[2][i])
                export_az.append(data[3][i])
                export_a.append (interp2(data[4][i-1],data[4][i],data[0][i-1],data[0][i],export_t[-1]))
                
    return([export_t,export_ax,export_ay,export_az,export_a,dt])
    
import numpy as np

def GetFFT(sample,dt):
    Ts = dt
    y = sample[1]
    n = len(y)                  # length of the signal
    k = np.arange(n)
    T = n*Ts
    frq = k/T                   # two sides frequency range
    frq = frq[range(int(n/2))]  # one side frequency range
    Y = np.fft.fft(y)/n         # fft computing and normalization
    Y = Y[range(int(n/2))]
    return([frq,abs(Y)])

def Samples(filename,time_length):
    [t,ax,ay,az,a] = reading_acc_data(filename)
    [t_cl,ax_cl,ay_cl,az_cl,a_cl] = clerification([t,ax,ay,az,a])
    [t_norm, a_x_norm, a_y_norm, a_z_norm, a_norm,dtime] = normalization([t_cl,ax_cl,ay_cl,az_cl,a_cl])

    i=0
    while ((t_norm[i] - t_norm[0])<time_length):
        i+=1
    i_step = i
    i = i_step

    time_sample = []
    ax_sample = []
    ay_sample = []
    az_sample = []
    a_sample = []

    while i<len(t_norm):
        temp_time = []
        for j in range(i-i_step,i):
            temp_time.append(t_norm[j]-t_norm[i])
        time_sample.append(temp_time)
        ax_sample.append(a_x_norm[i-i_step:i])
        ay_sample.append(a_y_norm[i-i_step:i])
        az_sample.append(a_z_norm[i-i_step:i])
        a_sample.append(a_norm[i-i_step:i])
        i += i_step

    return([time_sample,ax_sample,ay_sample,az_sample,a_sample])

def SimCos(x,y):
    a = 0.0
    b = 0.0
    c = 0.0
    if(len(x)==len(y)):
        for i in range(len(x)):
            a+=x[i]*y[i]
            b+=x[i]**2
            c+=y[i]**2
        try:
            sc = a/(sqrt(b)*sqrt(c))
        except(ValueError):
            sc=0
    else:
        sc = 0
    return(sc)

def CosSimScan(filename, sample):
    [t,ax,ay,az,a] = reading_acc_data(filename)
    [t_cl,ax_cl,ay_cl,az_cl,a_cl] = clerification([t,ax,ay,az,a])
    [t_norm, a_x_norm, a_y_norm, a_z_norm, a_norm,dtime] = normalization([t_cl,ax_cl,ay_cl,az_cl,a_cl])
    ax_sim = []
    ay_sim = []
    az_sim = []
    a_sim = []
    t_sim = []
    for i in range(len(t_norm)-len(sample[0])):
        ax_sim.append(SimCos(a_x_norm[i:i+len(sample[1])],sample[1]))
        ay_sim.append(SimCos(a_y_norm[i:i+len(sample[2])],sample[2]))
        az_sim.append(SimCos(a_z_norm[i:i+len(sample[3])],sample[3]))
        a_sim.append(SimCos(a_norm[i:i+len(sample[4])],sample[4]))
        t_sim.append(t_norm[i])
    return([t_sim,ax_sim,ay_sim,az_sim,a_sim])


def FFTFromFile(filename):
    [t,ax,ay,az,a] = reading_acc_data(filename)
    [t_cl,ax_cl,ay_cl,az_cl,a_cl] = clerification([t,ax,ay,az,a])
    [t_norm, a_x_norm, a_y_norm, a_z_norm, a_norm,dtime] = normalization([t_cl,ax_cl,ay_cl,az_cl,a_cl])
    [freq_a, ampl_a] = GetFFT([t_norm,a_norm],dtime)
    [freq_ax,ampl_ax] = GetFFT([t_norm,a_x_norm],dtime)
    [freq_ay,ampl_ay] = GetFFT([t_norm,a_y_norm],dtime)
    [freq_az,ampl_az] = GetFFT([t_norm,a_z_norm],dtime)
    return([freq_a,ampl_a,freq_ax,ampl_ax,freq_ay,ampl_ay,freq_az,ampl_az])

def FFTFromFileSequences(filenames, time_length):
    a_sampl = []
    t_sampl = []
    for i in range(len(filenames)):
        [time_sample, ax_sample, ay_sample, az_sample, a_sample] = Samples(filenames[i],time_length)
        t_sampl += time_sample
        a_sampl += a_sample
    
    freq = []
    ampl = []
    for i in range(len(t_sampl)):
        [freq_a, ampl_a] = GetFFT([t_sampl[i],a_sampl[i]],(t_sampl[i][1]-t_sampl[i][0]))
        freq.append(freq_a)
        ampl.append(ampl_a)
    return([freq,ampl])
