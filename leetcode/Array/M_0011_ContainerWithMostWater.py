class Solution:
    def maxArea(self, height: List[int]) -> int:
        #index*index*min(height[index],height[index])
        water=0
        left=0
        right=len(height)-1
        while left<right:
            area=(right-left)*min(height[left],height[right])
            if height[left]>height[right]:
                right-=1
            else:
                left+=1
            water=max(area,water)
        return water