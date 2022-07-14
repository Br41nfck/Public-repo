# Two sum
# Description:
# nums = [2,7,11,15], target = 9
# Output = [0,1], because [0] + [1] = 2 + 7 = 9

def two_sum(nums, target):
    d = {}
    for i, n in enumerate(nums):
        m = target-n
        if m in d:
            return [d[m], i]
        else:
            d[n] = i

ans = two_sum([2,7,11,15], 13)
print(ans)