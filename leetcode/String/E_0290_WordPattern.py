class Solution:
    def wordPattern(self, pattern: str, s: str) -> bool:
        words=s.split(' ')
        dp={}
        dw={}
        if len(words)!=len(pattern):
            return False
        for i in range(len(words)):
            p=pattern[i]
            w=words[i]
            if (p in dp and w!=dp[p]) or (w in dw and p!=dw[w]):
                return False
            else:
                dp[p]=w
                dw[w]=p
        return True
            