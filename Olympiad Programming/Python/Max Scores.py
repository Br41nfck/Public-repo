def solution(arr):
    lo = arr[0]
    hi = arr[0]
    lob = 0
    hib = 0
    for i in range(1,len(arr)):
        if arr[i] < lo:
            lob += 1
            lo = arr[i]
        if arr[i] > hi:
            hib += 1
            hi = arr[i]
    return [hib, lob]