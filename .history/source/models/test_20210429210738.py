import matplotlib.pyplot as plt 
import numpy as np
fig = plt.figure()
ax = fig.add_subplot(111)
x = [7e-06,1e-05,8e-05,1e-04,1e-03,1e-02]
y = [20,48,60,79,80,80]

#x = [1/i for i in x]
#y = [1/i for i in y]
#plt.xticks(np.arange(11))
#plt.yticks(np.arange(11))
plt.scatter(x,y,c='r')
plt.plot(x,y)

for xy in zip(x, y):                                       # <--
    ax.annotate('(%s, %s)' % xy, xy=xy, textcoords='data') # <--
#plt.xlim(min(x),max(x))
#plt.ylim(min(y),max(y))

#ax.set_xlim([6e-06,2e-02])
plt.grid()
plt.show()

