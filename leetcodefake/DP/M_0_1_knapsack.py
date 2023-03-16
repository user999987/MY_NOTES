'''
item0 
着重解释下数组下标含义
[[ 0. 15. 15. 15. 15.]
[ 0. 15. 15. 20. 35.]
[ 0. 15. 15. 20. 35.]]
dp[i][j] 是指在 背包重量 为 j 的情况下，怎么拿物品 0,1,2,3..i 得到的最大值
dp[i-1][j] 显然就是不拿(或者不能拿 拿了就超重) 物品 i 的情况下 最大值 只能是 物品
0~i-1 重量 j 的情况下的最大值 
dp[i-1][j-weight[i]] 是什么呢？是当你发现在重量允许的情况下 你可以拿 i 了 但是 这个
时候 你要知道 物品 0~i-1 在重量为 j-weight[i] 的情况下 的最大值, 
然后选择 最大的那个 给 dp[i][j]
'''
import numpy as np
def zeroOneDP(weights, values, capacity):
    dp = np.zeros((len(value)+1, limit+1))
    dp[:,0] = 0
    for i in range(1,len(weight)+1):
        for j in range(1,limit+1):
            if j<weight[i-1]:
                dp[i][j] = dp[i-1][j]
            else:
                
                opt_in = dp[i-1][j-weight[i-1]]+value[i-1]
                opt_out = dp[i-1][j]
                dp[i][j] = max(opt_in,opt_out)
    print(dp)
if __name__ == "__main__":

    weight = [1, 3, 5]
    value = [15, 20, 30]

    limit = 4
    zeroOneDP(weight, value, limit)


def numberOfWaysToMakeChange(n, coins):
    # Write your code here.
    size = len(coins)

    # Declaring a 2-D array
    # for storing solutions to subproblems:

    arr = [[0] * (n + 1) for x in range(size + 1)]
    # Initializing first column of array to 1
    # because a sum of 0 can be made
    # in one possible way: {0}
    for i in range(size + 1):
        arr[i][0] = 1

    # Applying the recursive solution:
    for i in range(1, size + 1):
        for j in range(1, n + 1):
            if coins[i - 1] > j:  # Cannot pick the highest coin:
                arr[i][j] = arr[i - 1][j]
            else:  # Pick the highest coin:
                arr[i][j] = arr[i - 1][j] + arr[i][j - coins[i - 1]]

    return arr[size][n]