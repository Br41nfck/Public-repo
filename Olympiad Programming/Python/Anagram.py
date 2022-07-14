# Anagram
# Input: game, mega
# Output: True, because 'mega' is anagram of 'game'
# Input: bear, beer
# Output: False, because 'beer' is not anagram of 'bear'
def anagram(s,t):
   
   dic = {}
   
   for i in s:
        if i not in dic:
            dic[i] = 1
        else:
            dic[i] += 1
    
   for j in t:
        if j not in dic:
            return False
        else:
            dic[j] -= 1
    
   for value in dic.values():
        if value != 0:
            return False
    
   return True
    
s = 'game'
t = 'mega'
ans = anagram(s,t)
print(ans) # True
s = 'bear'
t = 'beer'
ans = anagram(s,t)
print(ans) # False