class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        n=len(nums)
        if not nums or n<3:
            return []
        nums.sort()
        res=[]

        for i in range(n):
            if nums[i]>0:
                return res
            if i>0 and nums[i]==nums[i-1]:
                continue
            left=i+1
            right=n-1
            while left<right:
                L=nums[left]
                R=nums[right]
                temp=nums[i]
                if L+R+temp==0:
                    left+=1
                    right+=1
                    while (left<right and nums[left]==nums[left-1]):
                        left+=1
                    while (left<right and nums[right]==nums[right+1]):
                        right-=1
                elif L+R+t>0:
                    right-=1
                elif L+R+t<0:
                    left+=1
        return res