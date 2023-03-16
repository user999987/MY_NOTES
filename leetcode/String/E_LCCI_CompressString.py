class Solution:
    def compressString(self, S: str) -> str:
        n = len(S)
        if n == 0:
            return S
        i, s, counter, flag = 0, '', 0, S[0]
        while i < n:
            if S[i] != flag:
                s += flag + str(counter)
                counter = 1
                flag = S[i]
            else:
                counter += 1
            i += 1
        s += flag + str(counter)
        if len(s) < len(S):
            return s
        else:
            return S
