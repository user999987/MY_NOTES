class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        productNoZero=1
        zeros=0
        res=[]
        for v in nums:
            if v==0:
                product=0
                zeros+=1
            else:
                productNoZero*=v
        
        for v in nums:
            if v==0:
                if zeros>1:
                    res.append(0)
                else:
                    res.append(productNoZero)
            else:
                if zeros==0:
                    # Notice: productNoZero/v is a float
                    res.append(productNoZero/v)
                else:
                    res.append(0)
        return res