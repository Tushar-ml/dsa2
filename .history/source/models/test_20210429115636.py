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
intervals = list(hashmap.values())
merged_interval = []
merged_interval.append(intervals[0])

for int in intervals[1:]:
    x1,y1 = int
    x0,y0 = merged_interval[-1]
    if y0>=x1:
        merged_interval[-1][1] = max(y0,y1)
    else:
        merged_interval.append(int)
res = [y-x+1 for x,y in merged_interval]
print(res)