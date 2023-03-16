class Solution:
    def longestPalindrome(self, s: str) -> str:
        result=''
        for i,v in enumerate(s):
            odd=v
            l=i-1
            r=i+1
            while l>=0 and r<len(s) :
                if s[l]==s[r]:
                    odd=s[l]+odd+s[r]
                    l=l-1
                    r=r+1
                else:
                    print(odd)
                    break
            even=''
            l=i
            r=i+1
            while l>=0 and r<len(s):
                if s[l]==s[r]:
                    even=s[l]+even+s[r]
                    l=l-1
                    r=r+1
                else:
                    print(even)
                    break
            res = max(odd,even,key=lambda x: len(x))
            result = max(res, result, key=lambda x:len(x))
        return result
    

