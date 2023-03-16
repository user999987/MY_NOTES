# sliding window
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        left=0
        window=set()
        mmax=0
        for i, v in enumerate(s):
            while v in window:
                window.remove(s[left])
                left+=1
            window.add(v)
            mmax=max(len(window),mmax)
        return mmax
# 暴力
    def lengthOfLongestSubstringT(self, s: str) -> int:
        r=0
        for i,v in enumerate(s):
            ts=s[i]
            j=i+1
            while j<len(s):
                if s[j] in ts:
                    break
                else:
                    ts+=s[j]
                j+=1
            r=max(len(ts),r)
        return r
        