import matplotlib.pyplot as plt 

x = [7e-06,8e-05,1e-05,1e-04,1e-03,1e-02]
y = [20,48,60,79,80,80]
plt.xticks(np.arange(11))
plt.yticks(np.arange(11))
plt.scatter(x,y,c='r')
plt.plot(x,y)
plt.xscale()
#plt.xlim(min(x),max(x))
#plt.ylim(min(y),max(y))
plt.show()