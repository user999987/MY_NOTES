class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        n=len(nums)
        dp=n*[-10001]
        dp[0]=nums[0]
        for i in range(1,n):
            dp[i]=max(nums[i],dp[i-1]+nums[i])
        res=-10001
        for i in range(n):
            res=max(res,dp[i])
        return res