'''

[[1, 0, 0, 0, 0, 0, 0, 0], 
[1, 0, 1, 0, 1, 0, 1, 0], 
[1, 0, 1, 1, 1, 1, 2, 1], 
[1, 0, 1, 1, 2, 1, 3, 2], 
[1, 0, 1, 1, 2, 1, 3, 3]]
'''
def numberOfWaysToMakeChange(amount, coins):
    # Write your code here.
    n = len(coins)
    d = [[0]*(amount+1) for _ in range(n+1)]
    for i in range(n+1):
        d[i][0]=1
    for i in range(1, n+1):
        for j in range(1,amount+1):
            if coins[i-1]>j:
                d[i][j] = d[i-1][j]
            else:
                d[i][j] = d[i][j-coins[i-1]]+d[i-1][j]
    
    return d[-1][-1]

def numberOfWaysToMakeChange(amount, coins):
    d=[0]*(amount+1)
    d[0]=1
    n=len(coins)
    for i in range(1,n+1):
        for j in range(coins[i-1],amount+1):
            d[j]=d[j]+d[j-coins[i-1]]
    return d[-1]