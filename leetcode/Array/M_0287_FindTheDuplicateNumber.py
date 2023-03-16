class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        for i,v in enumerate(nums):
            if nums[abs(v)-1]<0:
                return abs(v)
            else:
                nums[abs(v)-1]*=(-1)
        return -1
    def findDuplicateT(self, nums: List[int]) -> int:
        x=set()
        for v in nums:
            if v in x:
                return v
            else:
                x.add(v)
        return -1