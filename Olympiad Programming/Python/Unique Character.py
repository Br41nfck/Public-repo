# First Unique Character in a string
# Input: programming
# Output: [0] = p 
# Input: ccooroollaa
# Output: [4] = r
# Input: www
# Output: -1

from collections import OrderedDict, Counter
def FirstUniqChar(s):
    for i,j in OrderedDict(Counter(s)).items():
        if j==1:
            return s.index(i), i
    return -1
    
ans = FirstUniqChar("ccooroollaa")
print(ans)