从凑零钱看DP问题:
1. 确定 base case: 目标金额 0， 返回 0，不需要硬币，目标金额小于 0，返回 -1 表示不科学
2. 明确选择 比如 凑零钱当中, 3个硬币 [1，2，5] 那么有3种选择 1 2 5
3. 确定状态 什么是状态 不是很好确定 但是选择好确定 确定了选择 就能找到状态 凑零钱当中 每次选取一个硬币之后 目标金额发生改变 改变的这个变量就是 状态
```python
def coin_change(coins: List,amount: int)->int:
    memo=[amount+1]*(amount+1)
    mmax = amount + 1
    def dp(coins: List,amount: int,mmax: int)->int:
        if amount==0: return 0
        if amount<0 : return -1
        if memo[amount]!=mmax: return memo[amount]

        res=float('inf')
        for coin in coins:
            sub_res=dp(coins, amount-coin,mmax)
            if sub_res==-1: continue
            res=min(sub_res+1,res)
        memo[amount]=-1 if res==float('inf') else res
        return memo[amount]
    return dp(coins,amount,mmax)
```