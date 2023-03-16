class Solution:
    def firstUniqChar(self, s: str) -> int:
        d={}
        for v in s:
            d[v]=d.get(v,0)+1
        for i in range(len(s)):
            if d[s[i]]==1:
                return i
        return -1