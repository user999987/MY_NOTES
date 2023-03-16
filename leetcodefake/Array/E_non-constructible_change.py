'''
coins=[]-> 1
coins=[1,2,4]-> 8
coins=[1,3,4]-> 2
coins=[2,2]-> 1
coins=[2,3]-> 1
coins=[1,2,3,4,20]-> 11
'''

def nonConstructibleChange(coins):
	# Write your code here.
	coinSum=0
	coins.sort()
	for coin in coins:
		if coin > coinSum+1:
			return coinSum+1
		coinSum+=coin
	return coinSum+1