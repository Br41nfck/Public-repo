# Squares of a Sorted Array
def sortedSquares(nums):
        for i in range(len(nums)):
            nums[i] = nums[i]*nums[i]
        nums.sort()
        return nums


ans = sortedSquares([-4,-1,0,3,10])
print(ans) # [0,1,9,16,100]