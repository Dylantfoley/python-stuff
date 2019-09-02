def pairOfZeroSum(nums):
    ans = []
    jns = []
    j = 0
    for i in range(j,len(nums)):
        for j in range(i+1, len(nums)):
            if (nums[i] == -nums[j]):
                ans.append(nums[i])
                ans.append(nums[j])
    jns.append(max(ans))
    jns.append(min(ans))
    return jns

nums2 = [2, 7, 9, -2]
x =pairOfZeroSum(nums2)
print(x)