# Description 
# Input data: array 
# Output data: True or False
# If there are two elements such that 
# their product is equal to any element,
# then it will return true, otherwise false.
# Used "collections" library.
from collections import *
def checkIfExist(array) -> bool:
    d = Counter(array)
    return any(2*x in d and (x != 2*x or d[x] > 1) for x in arr)
    
ans = checkIfExist([10,2,5,3]) # 2 * 5 = 10
ans_wrong = checkIfExist([2,3,5]) # No one
print(ans)
print(ans_wrong)