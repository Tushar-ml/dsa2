'''import matplotlib.pyplot as plt 
import numpy as np
x = [7e-06,8e-05,1e-05,1e-04,1e-03,1e-02]
y = [20,48,60,79,80,80]
#plt.xticks(np.arange(11))
#plt.yticks(np.arange(11))
plt.scatter(x,y,c='r')
plt.plot(x,y)

#plt.xlim(min(x),max(x))
#plt.ylim(min(y),max(y))

ax = plt.gca()
ax.set_ylim([10,90])
#ax.set_xlim([6e-06,2e-02])
plt.show()'''

import collections
import pprint
s = "ababcbacadefegdehijhklij"

hashmap = collections.OrderedDict()
for idx,char in enumerate(s):
    if char not in hashmap:
        hashmap[char] = []
    hashmap[char].append(idx)
    hashmap[char] = [hashmap[char][0],hashmap[char][-1]]
pprint.pprint(hashmap)
res = []
