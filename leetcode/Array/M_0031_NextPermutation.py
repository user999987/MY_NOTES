class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        n=len(nums)
        i=n-2
        j=n-1
        k=n-1
        while i>=0 and nums[i]>=nums[j]:
            i-=1
            j-=1
        # tail up
        if j==n-1:
            nums[i],nums[j]=nums[j],nums[i]
            return nums
        if i==-1:
            return nums.reverse()
        while k>j and nums[k]<=nums[i]:
            k-=1
        nums[i],nums[k]=nums[k],nums[i]
        nums[j:]=reversed(nums[j:])
        return nums