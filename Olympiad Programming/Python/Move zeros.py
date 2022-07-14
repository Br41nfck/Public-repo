# Move Zeros
# Input: nums = [0,1,0,3,12]
# Output: nums = [1,3,12,0,0]

def move_zeros(array):
    i = 0
    for j in range(len(array)):  
        if array[j] != 0:
            array[i], array[j] = array[j], array[i] # Swap
            i = i + 1 # Increase, if done
    return array
    
ans = move_zeros([0,1,0,3,12])
print(ans)