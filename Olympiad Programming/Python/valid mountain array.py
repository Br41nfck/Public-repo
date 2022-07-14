def validMountainArray(array) -> bool:
        if len(array) < 3: return False;
        l = 0;
        r = len(array) - 1
        while l + 1 < len(array) - 1 and array[l] < array[l + 1]: 
            l += 1
        while r - 1 > 0 and array[r] < array[r - 1]: 
            r -= 1
        return l == r


ans = validMountainArray([0,3,2,1])
print(ans)