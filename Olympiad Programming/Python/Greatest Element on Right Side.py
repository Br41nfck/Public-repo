# Input: arr = [17,18,5,4,6,1]
# Output: arr = [18,6,6,6,6,1,-1]

def GEonRS(arr):
        m = -1
        i = len(arr) -1 
        while i >= 0:
            tmp = arr[i]
            arr[i] = m
            if tmp > m:
                m = tmp
            i-= 1
        return arr

ans = GEonRS([17,18,5,4,6,1]) 
print(ans) # [18,6,6,6,6,1,-1]