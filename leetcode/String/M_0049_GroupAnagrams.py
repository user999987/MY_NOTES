class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        d={}
        for s in strs:
            ss=''.join(sorted(s))
            d[ss]=d.get(ss,[])
            d[ss].append(s)
        return list(d.values())