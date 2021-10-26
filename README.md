# Modelling of Near-Limit KEH systems. 

This software is a part of a PhD project **"Investigation and Optimisation of Kinetic Energy Harvesters with Nonlinear Electromechanical Coupling Mechanisms"**. It contains the software for the recording of an acceleration during the walking or running (for the M5Stack). It has the script for the analysis of the acceleration waveforms. Finally, it has the application for the efficiency of the learning algorithm estimation.  

All results were published:
**Near-Limit Kinetic Energy Harvesting From Arbitrary Acceleration Waveforms: Feasibility Study by the Example of Human Motion**
doi.org/10.1109/ACCESS.2020.3042388

## Requirements

* python >= 3.7
* jupyter lab >= 3.0
* numpy >= 1.18

## Usage

1. **M5Stack** software is in the corresponding folder. To run it, one needs to have the Arduino sketch writer. 
2. **Data** folder contains all datasets. 
3. **Acceleration processing** has the prepocessing software for the datasets. In addition, it has the scripts that calculate the cos-similarity of a different waveforms, the Liapunov exponents, Phase portraits and ARIMA model of the givel waveforms. 
4. **Efficiency Estimation** has the software that estimates the predictive algorithm efficiency, and maximal converted power of the system.   
