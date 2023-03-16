class Solution:
    def nextGreaterElements(self, nums: List[int]) -> List[int]:

        result = [-1]*len(nums)
        stack = []
        for i in range(len(nums)*2):
            idx = i%len(nums)
            while stack and nums[stack[-1]] < nums[idx]:
               result[stack.pop()] = nums[idx]    
            stack.append(idx)
        return result
