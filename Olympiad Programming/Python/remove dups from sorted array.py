def remove_dups(numbers):
    x = 1 
    for i in range(len(numbers)-1):
        if (numbers[i] != numbers[i+1]):
            numbers[x] = numbers[i+1]
            x = x + 1 
    return x
    
ans = remove_dups([1,2,3,3,3])
print(ans)