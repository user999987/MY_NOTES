'''
amount = 7
coins = [1,5,10]
[[0, inf, inf, inf, inf, inf, inf, inf], 
[0, 1, 2, 3, 4, 5, 6, 7], 
[0, 1, 2, 3, 4, 1, 2, 3], 
[0, 1, 2, 3, 4, 1, 2, 3]]
'''
def minNumberOfCoinsForChange(amount, coins):
    # Write your code here.
	n=len(coins)
	d = [ [0]*(amount+1) for _ in range(n+1) ]
	for i in range(1,amount+1):
		d[0][i] = float("inf")
	for i in range(1,n+1):
		for j in range(1,amount+1):
			if j<coins[i-1]:
				d[i][j] = d[i-1][j]
			else:
				d[i][j] = min(d[i-1][j],d[i][j-coins[i-1]]+1)
	print(d)
	return -1 if d[-1][-1] == float("inf") else d[-1][-1]

'''
[0, inf, inf, inf, inf, inf, inf, inf]
[0, 1, 2, 3, 4, 5, 6, 7]
[0, 1, 2, 3, 4, 1, 2, 3]
[0, 1, 2, 3, 4, 1, 2, 3]
'''
def minNumberOfCoinsForChange(amount, coins):
    # Write your code here.
	n = len(coins)
	d = [float("inf")]*(amount+1)
	d[0]=0
	print(d)
	for i in range(1,n+1):
		for j in range(coins[i-1],amount+1):
			d[j] = min(d[j],d[j-coins[i-1]]+1)
		print(d)
	return d[-1] if d[-1]!=float("inf") else -1
