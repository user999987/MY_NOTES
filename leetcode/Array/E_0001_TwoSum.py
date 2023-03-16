class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        d={}
        for i,v in enumerate(nums):
            if target-v not in d:
                d[v]=i
            else:
                return [i,d[target-v]]
                