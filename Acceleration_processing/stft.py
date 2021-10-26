from tftb.processing import ShortTimeFourierTransform
import numpy as np
import matplotlib.pyplot as plt
from tftb.generators import fmconst

from math import cos, sin

signal = []
for i in range(2000):
	signal.append(10*sin(0.001*i)+2*sin(0.002*i)+10*sin(0.01*i)+2*sin(0.02*i))

signal = np.array(signal)

stft = ShortTimeFourierTransform(signal)
stft.run()
stft.plot()