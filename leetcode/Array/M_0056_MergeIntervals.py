class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort()
        res=[]
        for v in intervals:
            if not res or res[-1][1]<v[0]:
                res.append(v)
            else:
                res[-1][1]= max(res[-1][1],v[1])
        return res