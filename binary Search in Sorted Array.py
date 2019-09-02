def binarySearchSortedArray(nums, s):
    numsLower = nums[:len(nums)//2]
    numsUpper = nums[len(nums)//2:]
    if s<= numsLower[0]:
        for i in range(len(numsLower)):
            if s == numsLower[i]:
                return True
    else:
        for i in range(len(numsUpper)):
            if s == numsUpper[i]:
                return True
    return False
nums = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
x = binarySearchSortedArray(nums, 15)
print(x)