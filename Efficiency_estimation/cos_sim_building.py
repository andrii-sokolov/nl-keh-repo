from data_processing import Samples, CosSimScan, SimCos
import random


def Build_CosSimFile(filename,samplename,time_length):
    [ts,axs,ays,azs,a_s] = Samples(samplename,time_length)    
    container_t = []
    container_ax = []
    container_ay = []
    container_az = []
    container_a = []
    for i in range(len(ts)):
        [timesim,axsim,aysim,azsim,asim] = CosSimScan(filename,[ts[i],axs[i],ays[i],azs[i],a_s[i]])
        container_t.append(timesim)
        container_ax.append(axsim)
        container_ay.append(aysim)
        container_az.append(azsim)
        container_a.append(asim)
        print("sequence \t"+str(i)+" of "+str(len(ts)))
    axfile = open("export_ax_similarity.dat","w")
    ayfile = open("export_ay_similarity.dat","w")
    azfile = open("export_az_similarity.dat","w")
    afile = open("export_a_similarity.dat","w")
    timefile = open("export_time.dat","w")
    for i in range(len(container_t[0])):
        for j in range(len(container_t)):
            timefile.write(str(container_t[j][i])+"\t")
            axfile.write(str(container_ax[j][i])+"\t")
            ayfile.write(str(container_ay[j][i])+"\t")
            azfile.write(str(container_az[j][i])+"\t")
            afile.write(str(container_a[j][i])+"\t")
        timefile.write("\n")
        axfile.write("\n")
        ayfile.write("\n")
        azfile.write("\n")
        afile.write("\n")
    axfile.close()
    ayfile.close()
    azfile.close()
    afile.close()
    timefile.close()

import csv                #importing library for *.csv files processing
import numpy as np

def read_sim_from_data(time_filename, ax_filename, ay_filename, az_filename, a_filename):
    ft = open(time_filename,"r")
    out_time_rev = []
    with open(time_filename) as ft:
        datareader = csv.reader(ft, delimiter="\t")                 #setting separation symbol as TAB
        for line in datareader:                                           #writing the data on prepeared lists: 
            out_time_rev.append([])
            try:
                for word in line:
                    out_time_rev[-1].append(float(word))
            except(ValueError):
                pass
    out_time = list(np.transpose(np.array(out_time_rev)))
    out_ax_rev = []
    with open(ax_filename) as fax:
        datareader = csv.reader(fax, delimiter="\t")                 #setting separation symbol as TAB
        for line in datareader:                                           #writing the data on prepeared lists: 
            out_ax_rev.append([])
            try:
                for word in line:
                    out_ax_rev[-1].append(float(word))
            except(ValueError):
                pass
    out_ax = list(np.transpose(np.array(out_ax_rev)))
    out_ay_rev = []
    with open(ay_filename) as fay:
        datareader = csv.reader(fay, delimiter="\t")                 #setting separation symbol as TAB
        for line in datareader:                                           #writing the data on prepeared lists: 
            out_ay_rev.append([])
            try:
                for word in line:
                    out_ay_rev[-1].append(float(word))
            except(ValueError):
                pass
    out_ay = list(np.transpose(np.array(out_ay_rev)))
    out_az_rev = []
    with open(az_filename) as faz:
        datareader = csv.reader(faz, delimiter="\t")                 #setting separation symbol as TAB
        for line in datareader:                                           #writing the data on prepeared lists: 
            out_az_rev.append([])
            try:
                for word in line:
                    out_az_rev[-1].append(float(word))
            except(ValueError):
                pass
    out_az = list(np.transpose(np.array(out_az_rev)))
    out_a_rev = []
    with open(a_filename) as fa:
        datareader = csv.reader(fa, delimiter="\t")                 #setting separation symbol as TAB
        for line in datareader:                                           #writing the data on prepeared lists: 
            out_a_rev.append([])
            try:
                for word in line:
                    out_a_rev[-1].append(float(word))
            except(ValueError):
                pass
    out_a = list(np.transpose(np.array(out_a_rev)))
    return([out_time, out_ax, out_ay, out_az, out_a])


def FitSignals(time, ax, ay, az, a):
    ref_signal = a[0][3000:(len(a[0])-3000)]
    set_of_j = []
    temp_time = [time[0][3000:(len(a[0])-3000)]]
    temp_a = [ref_signal]
    for i in range(1,(len(a))):
        cs = 0.0
        j_found = 0
        for j in range(3000):
            temp = SimCos(ref_signal,a[i][j:(j+len(ref_signal))])
            if cs<temp:
                cs = temp
                j_found = j
        set_of_j.append(j_found)
        temp_time.append(time[i][j_found:(j_found+len(ref_signal))])
        temp_a.append(a[i][j_found:(j_found+len(ref_signal))])
        print(i)
    return([temp_time,temp_a])
    

import matplotlib.pyplot as plt
from matplotlib.colors import LightSource, Normalize

def display_colorbar():
    [t,axs,ays,azs,asim] = read_sim_from_data("export_time.dat", "export_ax_similarity.dat", "export_ay_similarity.dat", "export_az_similarity.dat", "export_a_similarity.dat")
    #[times,a_s] = FitSignals(t, axs, ays, azs, asim)
    #[t,axs,ays,azs,asim] = read_sim_from_data("export_time.dat", "export_ax_similarity.dat", "export_ay_similarity.dat", "export_az_similarity.dat", "export_a_similarity.dat")
    #print(len(times[0]))
        
    y, x = np.mgrid[0:3600:3600j, 0:6455:6455j]

    print(len(y))
    z = []
    i = 0
    j = 0
    while (i<3599):
        a = []
        rn = random.randint(1,10)
        rn = 7000 + rn*100
        for k in range(rn,rn+6455):
            a.append(azs[j][k])
        z.append(a)
        i+=1
        if ((i+1)%200 ==0):
            j+=1
    z = np.array(z)
    
    cmap = plt.cm.copper
    ls = LightSource(315, 45)
    rgb = ls.shade(z, cmap)

    fig, ax = plt.subplots()
    ax.imshow(rgb, interpolation='bilinear')

    # Use a proxy artist for the colorbar...
    im = ax.imshow(z, cmap=cmap)
    im.remove()
    fig.colorbar(im)

    ax.set_title('Using a colorbar with a shaded plot', size='x-large')


#Build_CosSimFile("Data/running_pocket_3.csv","Data/walking_right_hand_3.csv",1.2)
display_colorbar()
plt.show()