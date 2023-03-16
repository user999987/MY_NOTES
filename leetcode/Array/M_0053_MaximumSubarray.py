class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        
        pre=0
        maxx=nums[0]
        for v in nums:
            pre=max(v,pre+v)
            maxx=max(pre,maxx)
        return maxx

    def maxSubArrayT(self, nums: List[int]) -> int:
        d=[0]*len(nums)
        d[0]=nums[0]
        maxx=nums[0]
        for i in range(1,len(nums)):
            d[i]=d[i-1]+nums[i] if d[i-1]>0 else nums[i]
            maxx=max(maxx,d[i])
        return maxx