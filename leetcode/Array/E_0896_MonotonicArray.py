class Solution:
    def isMonotonic(self, nums: List[int]) -> bool:
        up,down=0,0
        n=len(nums)
        if n==1 or n==2:
            return True
        for i in range(1,n):
            if nums[i-1]-nums[i]>0:
                down=1
            elif nums[i-1]-nums[i]<0:
                up=1
            if up==1 and down==1:
                return False
        return True