class Solution:
    def isValid(self, s: str) -> bool:
        result=[]
        pairs={
            ')':'(',
            '}':'{',
            ']':'[',
        }
        for v in s:
            if v in pairs:
                if result and result[-1]==pairs[v]:
                    result.pop()
                else:
                    result.append(v)
            else:
                result.append(v)
        return False if result else True