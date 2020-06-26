from numpy import genfromtxt
import numpy as np
import matplotlib.pyplot as plt

my_data = genfromtxt('experiment2.csv', delimiter=',')

hk = np.array(my_data[0])
best_first = np.array(my_data[1])
beam = np.array(my_data[2])
best_first_restart = np.array(my_data[3])
beam_restart = np.array(my_data[4])

best_first -= hk
beam -= hk
best_first_restart -= hk
beam_restart -= hk

# Plot the SSSO data
# An "interface" to matplotlib.axes.Axes.hist() method
n, bins, patches = plt.hist(label="Best First", histtype='step',x=best_first, bins='auto', color='#0504aa',
                            alpha=0.7, rwidth=1.0)
n, bins, patches = plt.hist(label="Beam Search", histtype='step',x=beam, bins='auto', color='#B67EFA',
                            alpha=0.7, rwidth=1.0)
n, bins, patches = plt.hist(label="Best First Restart", histtype='step',x=best_first_restart, bins='auto', color='#4C4F56',
                            alpha=0.7, rwidth=1.0)
n, bins, patches = plt.hist(label="Beam Search Restart", histtype='step',x=beam_restart, bins='auto', color='#FF0000',
                            alpha=0.7, rwidth=1.0)

plt.grid(axis='y', alpha=0.75)
plt.xlabel('Score Different From Held-Karp')
plt.ylabel('Frequency')
plt.title('Score Frequency of SSSO')

maxfreq = n.max()
# Set a clean upper y-axis limit.
plt.show()

exit(0)