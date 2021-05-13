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

class Solution:
    
    #Function to find the largest number after k swaps.
    def findMaximumNum(self,s,k):
        #code here
        idx = 0
        s = [i for i in s]
        while k:
            
            maxNum = s[idx]
            j = idx
            for i in range(idx+1,len(s)):
                if maxNum < s[i]:
                    maxNum = s[i]
                    j = i
                    
            if j!=idx:
                s[idx],s[j] = s[j],s[idx]
            
            k -= 1
            print(s)
            idx += 1
            
                
                
        s = ''.join(i for i in s)        
        return s

k = 4
s = "4551711527"
test = Solution()
print(test.findMaximumNum(s,k))