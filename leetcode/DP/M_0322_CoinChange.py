class Solution:
    # process([1,2,5],11)
    # = 1+ min(process([1,2,5],10), process([1,2,5],9), process([1,2,5],6))    
    def coinChange(self, coins: List[int], amount: int) -> int:
        
        def process(coins,amount):
            if amount==0:
                return 0
            if amount<0:
                return -1


            ans=float('inf')
            for coin in coins:
                subProcess = process(coins,amount-coin)
                print(subProcess)
                if subProcess ==-1:
                    continue
                ans = min(ans,subProcess+1)


            return ans if ans != float('inf') else -1
            
        return process(coins,amount)