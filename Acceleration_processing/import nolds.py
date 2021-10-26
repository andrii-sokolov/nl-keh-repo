import nolds

file = open("Data/Data5.lor","r")

export_graph = []

for line in file:
	try:
		export_graph.append(float(line))
	except:
		pass

print(len(export_graph))
aver = sum(export_graph)/len(export_graph)
for i in range(len(export_graph)):
	export_graph[i] -= aver


import matplotlib.pyplot as plt
plt.plot(export_graph)
plt.show()

h = nolds.lyap_e(export_graph,emb_dim = 4, matrix_dim=4, tau = 0.1)
h2 = nolds.lyap_r(export_graph,emb_dim = 4,tau = 0.01,debug_plot = True)	

print(h)
print(h2)