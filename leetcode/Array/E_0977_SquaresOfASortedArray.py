class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        n=len(nums)
        left=0
        right=n-1
        i=n-1
        res=[0]*n
        while i >= 0:
            lv=nums[left]*nums[left]
            rv=nums[right]*nums[right]
            if lv>=rv:
                res[i]=lv
                left+=1
            else:
                res[i]=rv
                right-=1
            i-=1
        return res