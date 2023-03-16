class Solution:
    def wordPatternMatch(self, pattern: str, s: str) -> bool:
        pattern_to_s={}
        str_set=set()
        def process(i, j):
            if len(pattern)==i and len(s)==j:
                return True
            if len(pattern)==i or len(s)==j:
                return False
            if pattern[i] in pattern_to_s:
                substr=pattern_to_s[pattern[i]]
                if s[j:j+len(substr)]==substr:
                    return process(i+1,j+len(substr))
                return False
            for k in range(j+1,len(s)+1):
                # range(x,n+1)只到n
                # s[x:n]只到n-1 所以需要len(s)+1
                substr=s[j:k]
                if substr not in str_set:
                    str_set.add(substr)
                    pattern_to_s[pattern[i]]=substr
                    if process(i+1,k):
                        return True
                    pattern_to_s.pop(pattern[i])
                    str_set.remove(substr)
            return False
        return process(0,0)


'''
比较特殊的变种
"pattern": "xxyxxy",
"string": "gogopowerrangergogopowerranger"
['go','powerranger']
you may see "xxxxx" or "yyyyy"本质上一样 为了减少算法复杂度 transform pattern start with y into x
'yyxy'->'xxyx'
'''
def patternMatcher(pattern, string):
    # Write your code here.\
    pattern, patternUpdated = patternUpdate(pattern)

    countX = pattern.count('x')
    countY = pattern.count('y')

    n = len(string)
    if countY != 0:
        indexY = -1 # indexY=2 means前面有俩X
        for i, v in enumerate(pattern):
            if v == 'y':
                indexY = i
                break
        lenX = 1
        while lenX < n and lenX * countX < n:
            if (n - lenX * countX) % countY != 0:
                lenX += 1
                continue
            lenY = int((n - lenX * countX) / countY)
            X = string[0:lenX]
            Y = string[lenX * indexY:lenY + lenX * indexY]

            newString = ''
            for p in pattern:
                if p == 'x':
                    newString += X
                else:
                    newString += Y

            if newString == string:
                return [X, Y] if patternUpdated == 0 else [Y, X]
            lenX += 1
        return []
    else:
        if len(string) % countX == 0:
            lenX = int(len(string) / countX)
            X = string[:lenX]
            if X * lenX == string:
                return [X, ""] if patternUpdated == 0 else ["", X]
        return []


def patternUpdate(pattern):
    if pattern[0] == 'y':
        # map looks like more high-end but string concatenation is more efficient
        pattern_list = list(map(lambda c: 'x' if c == 'y' else 'y', pattern))
        return ("".join(pattern_list), 1)
    else:
        return (pattern, 0)
