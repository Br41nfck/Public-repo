def thirdMax(array):
    m1 = m2 = m3 = -float("inf")
    for num in array:
        if num > m1:
            m1, m2, m3 = num, m1, m2
        elif m2 < num < m1:
            m2, m3 = num, m2
        elif m3 < num < m2:
            m3 = num
    
    return m3 if m3 > -float("inf") else m1

ans = thirdMax([1,2,3]) # 1 - third max
print(ans)