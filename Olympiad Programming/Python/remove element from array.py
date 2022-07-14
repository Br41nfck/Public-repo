def removeElement(numbers, value):
    i = 0
    for each in numbers:
        if each != value:
            numbers[i] = each
            i += 1 
    return i
  
ans = removeElement([3,2,2,3], 3)
print(ans)