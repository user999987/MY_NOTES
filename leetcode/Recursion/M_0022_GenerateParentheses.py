class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        res=[]
        leftp=0
        rightp=0

        def process(s,num,leftp,rightp,n):
            if leftp<rightp:
                return
            if leftp<=n:
                if num==0:
                    res.append(s)
                else:
                    process(s+'(',num-1,leftp+1,rightp,n)
                    process(s+')',num-1,leftp,rightp+1,n)
        process('',2*n,leftp,rightp,n)
        return res