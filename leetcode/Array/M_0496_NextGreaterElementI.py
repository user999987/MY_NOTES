class Solution:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        d={i:-1 for i in nums2}
        stack=[]
        res=[]
        for i,v in enumerate(nums2):
            while stack and nums2[stack[-1]]<v:
                d[nums2[stack.pop()]]=v
            stack.append(i)
        for i in nums1:
            res.append(d[i])
        return res