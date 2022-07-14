def findDisappearedNumbers(nums):
        out = []
        for i in nums:
            index = abs(i)-1
            nums[index] = abs(nums[index]) * -1
        for i,num in enumerate(nums):
            if num > 0:
                out.append(i+1)
        return out
        
ans = findDisappearedNumbers([1,3,4])