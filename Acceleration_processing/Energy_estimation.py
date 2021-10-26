from data_processing import Samples, reading_acc_data, clerification, normalization, SimCos
import numpy as np
import statistics

#Definition of the constants
#   The Energy extraction coefficient
K = 2.0*1000*0.025*0.001

def SamplesAligned(filename,time_length):
    '''
    Function allows to allign the samples with the maximal coherence 
    filename - the string with the filename of the data set
    time_length - the length of the sample
    '''
    
    # Reading of the data-set: 
    #   t - is the time sequence,
    #   ax- is the x-acceleration component,
    #   ay- is the y-acceleration component,
    #   az- is the z-acceleration component,
    #   a - is the total scalar acceleration. 
    [t,ax,ay,az,a] = reading_acc_data(filename)
    # The clarification of the data (removing the double points)
    [t_cl,ax_cl,ay_cl,az_cl,a_cl] = clerification([t,ax,ay,az,a])
    # Normalization of the datasets (complement the inexistant times)
    [t_norm, a_x_norm, a_y_norm, a_z_norm, a_norm,dtime] = normalization([t_cl,ax_cl,ay_cl,az_cl,a_cl])

    # Definition of the length of the time-stap
    i=0
    while ((t_norm[i] - t_norm[0])<time_length):
        i+=1
    i_step = i

    # Chosing of the reference time and acceleration as the middle-subsequence: 
    a_reference = a_norm[int(0.5*len(t_norm)-0.5*i_step):(int(0.5*len(t_norm)-0.5*i_step)+i_step)]
    t_reference = t_norm[int(0.5*len(t_norm)-0.5*i_step):(int(0.5*len(t_norm)-0.5*i_step)+i_step)]

    # Memory for the samples sequences:    
    time_sample = []
    ax_sample = []
    ay_sample = []
    az_sample = []
    a_sample = []

    # Definition of the number of subsequences:
    n_of_samples = int(len(t_norm)/i_step) -1
    for i in range(n_of_samples):
        # Similarity rating:
        sim = 0.0
        # The index of the subsequence's first element
        j_found = 0
        for j in range((i*i_step),(i*i_step+int(0.5*i_step))):
            # Definition of the cosine similarity:
            sim_a = SimCos(a_reference,a_norm[j:j+i_step])
            # Search for the maximal cosine similarity:
            if sim<sim_a:
                sim = sim_a
                j_found = j
        # Writing the subsequences to the answer:
        a_sample.append(a_norm[j_found:j_found+i_step])
        ax_sample.append(a_x_norm[j_found:j_found+i_step])
        ay_sample.append(a_y_norm[j_found:j_found+i_step])
        az_sample.append(a_z_norm[j_found:j_found+i_step])
    
    # Return the answer:
    return([t_norm[:i_step],ax_sample,ay_sample,az_sample,a_sample])

def LookForLocalMaxMin(t_samp,a_samp):
    '''
    Function allows to define the all local maximums and all local minimums in the signal
    t_samp - the time sample
    a_samp - the acceleration sample (May be the projection or the module)
    '''
    #   The index corresponds to found maximum sequence
    max_index = []
    #   The sequence of time points corresponding to the maximums
    max_t = []
    #   The sequence of acceleration points corresponding to the maximums
    max_a = []
    
    #   Search for the maximums:
    for i in range(1,len(a_samp)-1):
        if((a_samp[i-1]<a_samp[i])&(a_samp[i+1]<a_samp[i])):
            max_a.append(a_samp[i])
            max_t.append(t_samp[i])
            max_index.append(i)
    
    #   The same for the minimums:
    min_index = []
    min_t = []
    min_a = []
    for i in range(1,len(a_samp)-1):
        if((a_samp[i-1]>a_samp[i])&(a_samp[i+1]>a_samp[i])):
            min_a.append(a_samp[i])
            min_t.append(t_samp[i])
            min_index.append(i)
    return([max_index,max_t,max_a,min_index,min_t,min_a])

def EnergyEstimate(max_t, max_a, min_t, min_a, delta_a):
    '''
    Estimation of the maximal energy, produced by the harvester
    max_t - the sequence of the time maximums
    max_a - the sequence of the acceleration maximums
    min_t - the sequence of the time minimums
    min_a - the sequence of the acceleration minimums
    delta_a - the threshold of the energy  
    '''
    Energy = [0.0]      # Energy list (to write intermidiate energy)
    time_max = [0.0]    # time list (to write counted maximal times)
    time_min = [0.0]    # time list (to write counted minimal times)
    E = 0.0
    for i in range(len(max_t)):
        try:
            for j in range(len(min_t)):
                if (min_t[j]>max_t[i]):
                    if((max_a[i]-min_a[j])>delta_a):
                        E+= K*(max_a[i]-min_a[j])/(-max_t[i]+min_t[j])
                        Energy.append(E)
                        time_max.append(max_t[i])
                        time_min.append(min_t[j])
                    break
        except(IndexError):
            pass
    return([time_max, time_min, Energy])

def EnergyFromIndexes(sample_a, sample_t, time_min,time_max):
    sample = dict(zip(sample_t, sample_a))
    Energy = 0.0;
    for i in range(1,len(time_min)):
        Energy += K*(sample[time_max[i]] - sample[time_min[i]])
    return(Energy)

def PlotGraphOfSignal_Energy(filename, sample_time):
    [t,ax_sampl,ay_sampl,az_sampl,a_sampl] = SamplesAligned(filename, sample_time)
    [mai,max_t,max_a,mii,min_t,min_a] = LookForLocalMaxMin(t,a_sampl[8])
    [ti,tim,En]=EnergyEstimate(max_t,max_a,min_t,min_a,0.001)
    import matplotlib.pyplot as plt 
    plt.plot(t,a_sampl[8])
    plt.plot(ti,En)
    plt.plot(max_t,max_a,'o')
    plt.plot(min_t,min_a,'o')
    plt.show()

def PlotEnergyGraph(filename, sample_time,n_seq):
    [t,ax_sampl,ay_sampl,az_sampl,a_sampl] = SamplesAligned(filename, sample_time)
    [mai,max_t,max_a,mii,min_t,min_a] = LookForLocalMaxMin(t,a_sampl[n_seq])
    delta_xs = np.linspace(0.001,0.2,50)
    Energy = []
    Number_of_segments = []
    for delta_x in delta_xs:
        [ti,tim,En]=EnergyEstimate(max_t,max_a,min_t,min_a,delta_x)
        Energy.append(En[-1])
        Number_of_segments.append(len(En))
    return([Number_of_segments,Energy])

def PlotEnergyNormGraph(filename, sample_time):
    [t,ax_sampl,ay_sampl,az_sampl,a_sampl] = SamplesAligned(filename, sample_time)
    delta_xs = np.linspace(0.001,0.2,50)
    Norm_energ_seq = []
    Norm_n_seg_seq = []
    for i in range(len(ax_sampl)):
        [mai,max_t,max_a,mii,min_t,min_a] = LookForLocalMaxMin(t,a_sampl[i])
        Energy = []
        Number_of_segments = []
        for delta_x in delta_xs:
            [ti,tim,En]=EnergyEstimate(max_t,max_a,min_t,min_a,delta_x)
            Energy.append(En[-1])
            Number_of_segments.append(len(En))
        n_energy = []
        for i in range(len(Energy)):
            n_energy.append(Energy[i]/max(Energy))
        Norm_energ_seq.append(n_energy)
        Norm_n_seg_seq.append(Number_of_segments)
    return([Norm_n_seg_seq,Norm_energ_seq])

def EnergyExit(filename, sample_time,ind,th_hold):
    [t,ax_sampl,ay_sampl,az_sampl,a_sampl] = SamplesAligned(filename, sample_time)
    [mai,max_t,max_a,mii,min_t,min_a] = LookForLocalMaxMin(t,a_sampl[ind])
    [ti,tim,En]=EnergyEstimate(max_t,max_a,min_t,min_a,th_hold)
    ans = []
    for i in range(len(a_sampl)):
        [mai,max_t,max_a,mii,min_t,min_a] = LookForLocalMaxMin(t,a_sampl[i])
        [ti_1,tim_1,En]=EnergyEstimate(max_t,max_a,min_t,min_a,th_hold)
        EstimE = EnergyFromIndexes(a_sampl[i], t, tim,ti)
        ans.append(EstimE/En[-1])
    return(ans)

def GetAverage(filename_teach, filename_study, sample_time, th_hold):
    [t,ax_sampl,ay_sampl,az_sampl,a_sampl] = SamplesAligned(filename_teach, sample_time)
    [t1,ax_sampl1,ay_sampl1,az_sampl1,a_sampl1] = SamplesAligned(filename_study, sample_time)
    a_av = []
    for i in range(len(a_sampl[0])):
        av = 0.0
        for j in range(len(a_sampl)):
            av += a_sampl[j][i]
        a_av.append(av/len(a_sampl))
    [mai,max_t,max_a,mii,min_t,min_a] = LookForLocalMaxMin(t,a_av)
    [ti,tim,En] = EnergyEstimate(max_t,max_a,min_t,min_a,th_hold)

    export_max = [[],[]]
    export_min = [[],[]]
    export_sampl_max = [[],[]]
    export_sampl_min = [[],[]] 
    
    for i in range(len(ti)):
        for j in range(len(t)):
            try:
                if(t[j] == ti[i]):
                    export_max[0].append(ti[i])
                    export_max[1].append(a_av[j])
                    export_sampl_max[0].append(ti[i])
                    export_sampl_max[1].append(a_sampl[8][j])
                if(t[j] == tim[i]):
                    export_min[0].append(tim[i])
                    export_min[1].append(a_av[j])
                    export_sampl_min[0].append(ti[i])
                    export_sampl_min[1].append(a_sampl[8][j])
            except:
                pass
    ans = []
    for i in range(len(a_sampl)):
        [mai,max_t,max_a,mii,min_t,min_a] = LookForLocalMaxMin(t,a_sampl1[i])
        [ti_1,tim_1,En]=EnergyEstimate(max_t,max_a,min_t,min_a,th_hold)
        EstimE = EnergyFromIndexes(a_sampl1[i], t, tim,ti)
        ans.append(EstimE/En[-1])
    return([ans,export_max,export_min,[t,a_av],[t,a_sampl[8]],export_sampl_max,export_sampl_min])

def GetAverageAndError(filename, sample_time, th_hold):
    [t, ax_sampl, ay_sampl, az_sampl, a_sampl] = SamplesAligned(filename, sample_time)
    RelEnerg = []
    for i in range(len(a_sampl)):
        [mai, max_t, max_a, mii, min_t, min_a] = LookForLocalMaxMin(t, a_sampl[i])
        [ti, tim, En]=EnergyEstimate(max_t, max_a, min_t, min_a, th_hold)
        RelEnerg.append([])
        for j in range(len(a_sampl)):
            EstimE = EnergyFromIndexes(a_sampl[j], t, tim, ti)
            RelEnerg[-1].append(EstimE/En[-1])
    StandSigma = []
    AverEnerg = []
    for rel in RelEnerg:
        StandSigma.append(statistics.stdev(rel))
        AverEnerg.append(sum(rel)/len(rel))
    return([AverEnerg,StandSigma])

PlotGraphOfSignal_Energy("Data/walking_right_hand_2.csv", 1.4)

PlotGraphOfSignal_Energy("Data/running_pocket_2.csv", 0.8)