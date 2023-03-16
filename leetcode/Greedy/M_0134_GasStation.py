class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        if sum(gas)<sum(cost):
            return -1
        i=0
        tank=distance=start_city=0
        while i<len(gas):
            tank+=gas[i]
            distance+=cost[i]
            if tank<distance:
                tank=0
                distance=0
                start_city=i+1
            i+=1
        return start_city
            