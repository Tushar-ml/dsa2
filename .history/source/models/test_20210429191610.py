import matplotlib.pyplot as plt 
import numpy as np
x = [7e-06,8e-05,1e-05,1e-04,1e-03,1e-02]
y = [20,48,60,79,80,80]

x = [1/i for i in x]
y = [1/i for i in y]
#plt.xticks(np.arange(11))
#plt.yticks(np.arange(11))
plt.scatter(x,y,c='r')
plt.plot(x,y)

#plt.xlim(min(x),max(x))
#plt.ylim(min(y),max(y))

#ax.set_xlim([6e-06,2e-02])
plt.show()

