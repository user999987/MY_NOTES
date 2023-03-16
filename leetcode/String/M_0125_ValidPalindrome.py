class Solution:
    def isPalindrome(self, s: str) -> bool:
        loop_s=''
        diff= ord('a')-ord('A')
        for v in s:
            if 65<=ord(v)<=90:
                loop_s+=chr(ord(v)+diff)
            elif 97<=ord(v)<=122 or 48<=ord(v)<=57:
                loop_s+=v
        left=0
        right=len(loop_s)-1
        while left<right:
            if loop_s[left]!=loop_s[right]:
                return False
            else:
                left+=1
                right-=1

        return True
    
    def isPalindromeT(self, s: str) -> bool:

        loop_s=[ v.lower()  for v in s if v.isalnum() ]
        left=0
        right=len(loop_s)-1
        while left<right:
            if loop_s[left]!=loop_s[right]:
                return False
            else:
                left+=1
                right-=1

        return True