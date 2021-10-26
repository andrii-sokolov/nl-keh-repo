from data_processing import FFTFromFile, FFTFromFileSequences

[f,a] = FFTFromFileSequences(["Data/running_pocket_1.csv","Data/running_pocket_2.csv","Data/running_pocket_3.csv" ,"Data/running_pocket_1.csv"], 8.0)

import matplotlib.pyplot as plt 
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.gca(projection='3d')

dx = 1.0/len(f)
d = dx

for i in range(len(f)):
	z = []
	for j in range(len(a[i])):
		z.append(i)
	plt.plot(z[3:50],f[i][3:50],a[i][3:50], color = (d,0.0,1-d), linewidth = 0.8 )
	d += dx

plt.show()

def display_colorbar():
       
    y, x = np.mgrid[0:3600:3600j, 0:6455:6455j]
    [f,a] = FFTFromFileSequences(["Data/running_pocket.csv","Data/walking_right_hand_2.csv","Data/walking_right_hand_3.csv" ,"Data/walking_right_hand_4.csv"], 8.0)
    print(len(y))
    z = []
    i = 0
    j = 0
    while (i<3599):
        a = []
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
'''
display_colorbar()
plt.show()
'''