class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        phone={
            '2':['a','b','c'],
            '3':['d','e','f'],
            '4':['g','h','i'],
            '5':['j','k','l'],
            '6':['m','n','o'],
            '7':['p','q','r','s'],
            '8':['t','u','v'],
            '9':['w','x','y','z'],
        }
        res=[]

        def process(s,digits):
            if not digits:
                res.append(s)
            else:
                for letter in phone[digits[0]]:
                    process(s+letter,digits[1:])
        if not digits:
            return []
        process('',digits)
        return res